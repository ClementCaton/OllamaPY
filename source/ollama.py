import requests
from typing import overload
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
    @overload
    def generate(self, prompt:str)->str:
        """
        Generates a completion from a string using the model specified.\n
        `prompt` : a string, typically a question, used to generate the response.\n
        """
        answer = ''
        params = {'model': self.model, 'string': prompt, 'options': self.options}
        
        try:
            r = requests.post(f"http://{self.ip}:{self.port}/generate", json=params, stream=True)
            
            if r.status_code != 200:
                print('Error:', r.status_code)
                return
            
            for chunk in r.iter_content(chunk_size=None):
                answer += chunk.decode('utf-8')
            return answer

        except:
            print("Error: Could not connect to ollama server")
            return
    
    @overload
    def generate(self, prompt:str, model:str)->str:
        """
        Sets the object's model and generates a completion from a string using the model specified.\n
        `prompt` : a string, typically a question, used to generate the response.\n
        `model` : The model to use.\n
        """
        self.setModel(model)
        return self.generate(prompt)


    # Create a Model
    # need to know if possible when not running locally
    def createModel(self, model:str, path:str)->None:
        """
        Create a model on the ollama server (if running locally) using a Modelfile.
        """
        try:
            parameters = {'name':model, "path":path}
            requests.post(f'http://{self.ip}:{str(self.port)}/api/create', json=parameters)
        except:
            print("Error: Could not connect to ollama server")
            return

    # List Local Models
    def listLocalModels(self)->list:
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
    def showModelInfo(self, model:str)->dict:
        """Show details about a model including modelfile, template, parameters, license and system prompt."""
        try:
            parameters = {'name':model}
            r = requests.get(f'http://{self.ip}:{str(self.port)}/api/info', json=parameters)
            return r.json()
        except:
            print("Error: Could not connect to ollama server")
            return

    # Delete a Model
    def deleteModel(self, model:str)->None:
        """
        Delete a model from the ollama server.
        """
        try:
            parameters = {'name':model}
            requests.delete(f'http://{self.ip}:{str(self.port)}/api/delete', json=parameters)
        except:
            print("Error: Could not connect to ollama server")
            return

    # Pull a Model
    def __pull(self)->None:
        """
        Pull a model onto the ollama server.
        """
        try:
            parameters = {'name':self.model}
            requests.post(f'http://{self.ip}:{str(self.port)}/api/pull', json=parameters)
        except:
            print("Error: Could not connect to ollama server")
            return

    def setModel(self, model:str)->None:
        """
        Set the model to use.
        """
        self.model = model
        self.__pull()

    # Push a Model
    def pushModel(self, model:str)->None:
        """
        Upload a model to a model library. Requires registering for ollama.ai and adding a public key first.
        `model` : The name of the model to push.
        """
        try:
            parameters = {'name':model}
            requests.post(f'http://{self.ip}:{str(self.port)}/api/push', json=parameters)
        except:
            print("Error: Could not connect to ollama server")
            return


    # Generate Embeddings