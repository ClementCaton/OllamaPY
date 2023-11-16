import requests
from typing import Union
# TODO https://github.com/jmorganca/ollama/blob/main/docs/api.md

class Ollama:
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

    @property
    def __baseUrl(self)->str:
        return f"http://{self.ip}:{str(self.port)}/api"

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
            r = requests.post(f'{self.__baseUrl}/generate', json=params, stream=True)
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
    def createModel(self, model:str, path:str)->bool:
        """
        # NOT IMPLEMENTED\n
        Create a model on the ollama server (if running locally) using a Modelfile.\n
        `model` : The name of the model to create.\n
        `path` : The path to your Modelfile.\n
        """
        raise NotImplementedError

    # List Local Models
    def listLocalModels(self)->Union[str, None]:
        """List all the models on the ollama server."""
        try:
            r = requests.get(f'{self.__baseUrl}/tags')
            return r.json()
        except:
            print("Error: Could not connect to ollama server")
            return

    # Show Model Information
    def showModelInfo(self, model:str=None)->Union[dict, None]:
        """Show details about a model including modelfile, template, parameters, license and system prompt."""
        try:
            if model == None:
                model = self.model
            parameters = {'name':model}
            r = requests.post(f'{self.__baseUrl}/show', json=parameters)
            return r.content.decode("utf-8")
        except:
            print("Error: Could not get details about model")
            return
            #TODO Fix this

    # Delete a Model
    def deleteModel(self, model:str)->bool:
        """
        Delete a model from the ollama server.\n
        `model` : The exact name of the model to delete. Including ":version" if applicable.
        """


        for _model in self.listLocalModels()['models']:
            if _model['name'] == model:
                try:
                    parameters = {'name':model}
                    requests.delete(f'{self.__baseUrl}/delete', json=parameters)
                    return True
                except:
                    print("Error: Could not connect to ollama server")
                    return False
        print("Error: Model not found")
        return False

    # Pull a Model
    def __pull(self)->bool:
        """
        Pull a model onto the ollama server.
        """
        local = self.listLocalModels()
        if local == None or self.model not in local:
            try:
                parameters = {'name':self.model}
                requests.post(f'{self.__baseUrl}/pull', json=parameters)
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
        # NOT IMPLEMENTED\n
        Upload a model to a model library. Requires registering for ollama.ai and adding a public key first.\n
        `model` : The name of the model to push.
        """
        raise NotImplementedError

    # Generate Embeddings
    def embeddings(self, prompt:str, model:str=None, options:dict[str:any]=None):
        """
        Generate embeddings for a prompt using a model.\n
        `prompt` : Text to generate embeddings for.\n
        `model` : Name of model to generate embeddings from.\n
        `options` : Additional model parameters listed in the documentation for the Modelfile such as temperature.
        """
        if model != None:
            self.setModel(model)
        if options == None:
            options = {}
        try:
            parameters = {'model':self.model, 'prompt':prompt, 'options':options}
            r = requests.post(f'{self.__baseUrl}/embeddings', json=parameters)
            return r.content.decode("utf-8")
        except:
            print("Error: Could not connect to ollama server")
        return