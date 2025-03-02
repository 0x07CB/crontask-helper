#coding: utf-8

import requests

from typing import List
from typing import Dict
from typing import Union
from typing import Tuple
from typing import Optional
from typing import Any

from ollama import generate
from ollama._types import Options
from ollama import ChatResponse
from ollama import chat

from functions import write_formatted_crontask
from tools import write_formatted_crontask_tool


def model_unload(model: str, ollama_base_url: str):
    url = f"{ollama_base_url}/api/generate"
    payload = {
        "model": model,
        "keep_alive": 0
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print("Model unloaded successfully.")
    else:
        print(f"Failed to unload model. Status code: {response.status_code}, Response: {response.text}")

# Example usage
# model_unload("llama3.2", "http://localhost:11434")


# ######################################################### #


def generate_response(
    model: Optional[str] = "qwen2.5:0.5b",
    messages: Optional[List[Dict[str, Any]]] = None,
    tools: Optional[List[Dict[str, Any]]] = None,
    available_functions: Optional[Dict[str, Any]] = None,
    options: Optional[Options] = None,
    prompt: Optional[str] = None,
) -> str:
    """
    Generate a response from the model
    """
    
    if type(messages) == None: messages = [{'role': 'user', 'content': f'{prompt}'}]

    print('Prompt:', messages[0]['content'])

    response: ChatResponse = chat(
        model,
        messages=messages,
        tools=tools,
        options=options,
    )
  
    if response.message.tool_calls:
        # There may be multiple tool calls in the response
        for tool in response.message.tool_calls:
            # Ensure the function is available, and then call it
            if function_to_call := available_functions.get(tool.function.name):
                print('Calling function:', tool.function.name)
                print('Arguments:', tool.function.arguments)
                output = function_to_call(**tool.function.arguments)
                print('Function output:', output)
            else:
                print('Function', tool.function.name, 'not found')

    # Only needed to chat with the model using the tool call results
    if response.message.tool_calls:
        # Add the function response to messages for the model to use
        messages.append(response.message)
        messages.append({'role': 'tool', 'content': str(output), 'name': tool.function.name})

        # Get final response from model with function outputs
        final_response = chat(model, messages=messages, options=options)
        print('Final response:', final_response.message.content)

    else:
        print('No tool calls returned from model')
        

    return final_response.message.content


def ask_agent(
    prompt: Optional[str] = None,
    execute: Optional[str] = None,
    model: Optional[str] = "qwen2.5:0.5b",
    ollama_base_url: Optional[str] = "http://localhost:11434"
) -> str:
    """
    Ask the agent
    """
    messages_list = [
        {'role': 'system', 'content': "Agissez en tant qu'expert en configuration de tâches cron. Votre mission est de générer une ligne de configuration crontask correctement formatée. Respectez strictement le format suivant :\n\nMinute Hour Day Month Weekday command_to_be_executed\n\nUtilisez les opérateurs (*, -, /, ,) et les chaînes spéciales (@reboot, @daily, etc.) lorsque c'est nécessaire."},
        {'role': 'user', 'content': "Génère une ligne de configuration cron pour exécuter la commande '/bin/bash /opt/script1.sh' tous les jours à 07:00."}
    ]
    tools_list = [write_formatted_crontask_tool]
    prompt_ = None

    available_functions = {
        'write_formatted_crontask': write_formatted_crontask
    }

    # Configuration des options pour Ollama
    mes_options = Options(
        use_mlock=True,  # Utiliser mlock pour garder le modèle en mémoire
        use_mmap=True,   # Utiliser mmap pour charger le modèle
        num_gpu=200,     # Nombre de GPUs à utiliser
        temperature=0.3, # Température pour la génération
        num_thread=1,
        num_predict=300, # Nombre de réponses à générer
        keep_alive="20m",  # Garder le modèle en mémoire pendant 20 minutes (1200 secondes)
    )

    response = generate_response(
        model="qwen2.5:0.5b",
        messages=messages_list,
        tools=tools_list,
        available_functions=available_functions,
        options=mes_options,
        prompt=prompt_,
    )

    return response