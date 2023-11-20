# OllamaPY

OllamaPY is a Python library I did to use the Ollama API for my own projects. Feedback is appreciated.<br>
It's an interface, so it requires you to have Ollama running on a machine. You can download it [here](https://ollama.ai/download).<br>
It works with Python 3.11.4 and Ollama 0.1.10.

## Documentation

I copied parts of the documentation from the [Ollama API documentation](https://github.com/jmorganca/ollama/blob/main/docs/api.md) to describe the functions.

### Minimal examples
- Install models
```python
import ollama

client = ollama.Ollama()
# Setting a model for your instance will pull it from the ollama model library if it is not already installed
client.setModel("llama2")

# You can check if a model is already installed
print(client.listLocalModels())
```
- Get generate text 
```python
# This function will use the model you set for your instance
output = client.generate("Who are you ?")
# output is the JSON response string
print(output)

# You can also specify another model
output = client.generate("Who are you ?", "mistral:7b")
# output is the JSON response string
print(output)
```
- Here is a way to extract the text from the JSON response
```python
import json

def extract(generation:str)->str:
    text = ""
    generation = generation.split("\n")
    for line in generation[:-1]:
        text += json.loads(line)['response']
    return text
```

### Fonctions
- [generate(prompt, model)](https://github.com/jmorganca/ollama/blob/main/docs/api.md#generate-a-completion)
    - `prompt` : String
    - `model` (optional) : String
    - return : String or None

    Generate a response for a given prompt with a provided model.<br>
    Returns the JSON response from Ollama. If the model is not specified, it will use the model you set for your instance.<br>
    If the model specified or in your instance is invalid, or if the connection with Ollama fails, it will return None.

- [createModel(modelname:str, modelfile:str)](https://github.com/jmorganca/ollama/blob/main/docs/api.md#create-a-model)
    - `modelName` : String
    - `modelfile` : String
    - return : Boolean

    Create a model from a [Modelfile](https://github.com/jmorganca/ollama/blob/main/docs/modelfile.md).
    ## ! Not implemented yet !
    Returns True if the model was created, False otherwise.

- [listLocalModels()](https://github.com/jmorganca/ollama/blob/main/docs/api.md#list-local-models)
    - return : String

    It will return the JSON of the models that are available locally. If the connection with Ollama fails, it will return `None`.<br>
    You can use the extract function to get the list of models, but change `['response']` to `['models']`.

- [showModelInfo(model:str=None)](https://github.com/jmorganca/ollama/blob/main/docs/api.md#show-model-information)
    - `model` (optional) : String
    - return : String or None

    
    Show details about a model including modelfile, template, parameters, license, and system prompt.<br>
    If the model is not specified, it will use the model you set for your instance.<br>
    If the model specified or in your instance is invalid, or if the connection with Ollama fails, it will return None.

- [copyModel(modelInput:str, modelOutput:str)](https://github.com/jmorganca/ollama/blob/main/docs/api.md#copy-a-model)
    ## ! Not implemented yet !

- [deleteModel(model: str)](https://github.com/jmorganca/ollama/blob/main/docs/api.md#delete-a-model)
    - `model` : String

    Delete a model and its data.<br>
    Returns True if the model was deleted, False otherwise.

- [setModel(model:str)](https://github.com/jmorganca/ollama/blob/main/docs/api.md#pull-a-model)
    - `model` : String

    Set the model for your instance. It will pull it from the ollama model library if it is not already installed.<br>

- [pushModel()](https://github.com/jmorganca/ollama/blob/main/docs/api.md#push-a-model)

    ## ! Not implemented yet !

- [embeddings(prompt:str, model:str=None, option:dict[str,any]=None)](https://github.com/jmorganca/ollama/blob/main/docs/api.md#generate-embeddings)
    - `prompt` : String
    - `model` (optional) : String
    - `option` (optional) : dict[str,any]
    - return : String or None

## Installation
Copy paste the ollama.py file in your project and import it.<br>
(don't forget to star the repo if you like it, maybe one day it'll have pip support)