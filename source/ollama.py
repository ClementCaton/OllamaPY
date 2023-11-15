import requests
from typing import overload, Union
# TODO https://github.com/jmorganca/ollama/blob/main/docs/api.md

class ollama:
    """
    Instanciates a new [ollama](https://ollama.ai/) object.\n
    `ip` : The ip address of the ollama server. (localhost by default)\n
    `port` : The port of the ollama server. (11434 by default)\n
    `model` : The model name you want to use.\n
    `options` : The options you want to use.\n
    """
    def __init__(self)-> None:
        self.ip = "127.0.0.1"
        """
        Define the ip address of the ollama server
        """
        self.port = 11434
        """
        Define the port of the ollama server
        """
        self.model = ""
        """
        Define the model name you want to use
        """
        self.options = {}
        """
        Define the options you want to use
        """

    # Generate a completion
    def generate(self, prompt:str, model:str=None)->Union[str, None]:
        """
        Generates a completion from a string using the model specified.\n
        `prompt` : a string, typically a question, used to generate the response.\n
        """
        if model != None:
            self.setModel(model)
        answer = ''
        params = {'model': self.model, 'prompt': prompt}
        
        try:
            r = requests.post(f'http://{self.ip}:{str(self.port)}/api/generate', json=params, stream=True)
            if r.status_code != 200:
                print('Error:', r.status_code)
                return

            if r.encoding is None:
                r.encoding = 'utf-8'
            
            for line in r.iter_content(decode_unicode=True):
                if line:
                    answer += line
            return answer
        except:
            print("Error: Could not connect to ollama server")
            return

    # Create a Model
    # need to know if possible when not running locally
    def createModel(self, model:str, path:str)->bool:
        """
        Create a model on the ollama server (if running locally) using a Modelfile.
        """
        try:
            parameters = {'name':model, "path":path}
            requests.post(f'http://{self.ip}:{str(self.port)}/api/create', json=parameters)
            return True
        except:
            print("Error: Could not connect to ollama server")
            return False

    # List Local Models
    def listLocalModels(self)->Union[dict, None]:
        """
        List all the models on the ollama server.
        """
        try:
            r = requests.get(f'http://{self.ip}:{str(self.port)}/api/tags')
            return r.json()
        except:
            print("Error: Could not connect to ollama server")
            return

    # Show Model Information
    def showModelInfo(self, model:str)->Union[dict, None]:
        """Show details about a model including modelfile, template, parameters, license and system prompt."""
        try:
            parameters = {'name':model}
            r = requests.get(f'http://{self.ip}:{str(self.port)}/api/info', json=parameters)
            return r.json()
        except:
            print("Error: Could not connect to ollama server")
            return

    # Delete a Model
    def deleteModel(self, model:str)->bool:
        """
        Delete a model from the ollama server.
        """
        try:
            parameters = {'name':model}
            requests.delete(f'http://{self.ip}:{str(self.port)}/api/delete', json=parameters)
            return True
        except:
            print("Error: Could not connect to ollama server")
            return False

    # Pull a Model
    def __pull(self)->bool:
        """
        Pull a model onto the ollama server.
        """
        local = self.listLocalModels()
        if self.model not in local:
            try:
                parameters = {'name':self.model}
                requests.post(f'http://{self.ip}:{str(self.port)}/api/pull', json=parameters)
                return True
            except:
                print("Error: Could not connect to ollama server")
                return False
        else:
            return True

    def setModel(self, model:str)->None:
        """
        Set the model to use.
        """
        self.model = model
        self.__pull()

    # Push a Model
    def pushModel(self, model:str)->bool:
        """
        Upload a model to a model library. Requires registering for ollama.ai and adding a public key first.
        `model` : The name of the model to push.
        """
        try:
            parameters = {'name':model}
            requests.post(f'http://{self.ip}:{str(self.port)}/api/push', json=parameters)
            return True
        except:
            print("Error: Could not connect to ollama server")
            return False


    # Generate Embeddings