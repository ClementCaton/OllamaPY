import requests


class ollama:
    """
    Instanciates a new [ollama](https://ollama.ai/) object.
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
        self.model = "llama2"
        """
        Define the model name you want to use
        """
        self.options = {}
        """
        Define the options you want to use
        """

    # Generate a completion
    def generate(self, prompt:str, model:str)->str:
        """
        Sets the object's model and generates a completion from a string using the model specified.
        """
        self.setModel(model)
        return self.generate(prompt)

    def generate(self, prompt:str)->str:
        """
        Generate a completion from a string using the model specified in the ollama object.
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
    # Generate Embeddings