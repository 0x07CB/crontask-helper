#coding: utf-8

import requests

from typing import List
from typing import Dict
#from typing import Union
#from typing import Tuple
from typing import Optional
from typing import Any

#from ollama import generate
from ollama._types import Options
from ollama import ChatResponse
from ollama import chat

from functions import write_formatted_crontask
from tools import write_formatted_crontask_tool

from rich import print as rprint

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
        rprint("[bold green]Modèle déchargé avec succès.[/bold green]")
    else:
        rprint(f"[bold red]Erreur[/bold red]: [underline]Lors du déchargement du modèle[/underline]. Status code: {response.status_code}, Response: {response.text}")

# Example usage
# model_unload("llama3.2", "http://localhost:11434")


# ######################################################### #


def generate_response(
    model: Optional[str] = "llama3.2:3b",
    messages: Optional[List[Dict[str, Any]]] = None,
    tools: Optional[List[Dict[str, Any]]] = None,
    available_functions: Optional[Dict[str, Any]] = None,
    options: Optional[Options] = None,
    prompt: Optional[str] = None,
) -> str:
    """
    Generate a response from the model
    """
    
    if messages is None:
        messages = [{'role': 'user', 'content': f'{prompt}'}]

    rprint(f'[italic yellow]Prompt:[/italic yellow] {messages[-1]["content"]}')

    try:
        response: ChatResponse = chat(
            model,
            messages=messages,
            tools=tools,
            options=options,
        )
    except Exception as e:
        rprint(f"[bold red]Erreur[/bold red]: [underline]Lors de l'appel au modèle[/underline]: {e}")
        return f"Erreur: {e}"
  
    output = None
    final_response = response
    
    if response.message.tool_calls:
        rprint(f"[italic yellow]Le modèle a demandé {len(response.message.tool_calls)} appel(s) d'outil[/italic yellow]")
        
        # There may be multiple tool calls in the response
        for tool in response.message.tool_calls:
            # Ensure the function is available, and then call it
            if function_to_call := available_functions.get(tool.function.name):
                rprint(f'[italic yellow]Appel de la fonction:[/italic yellow] {tool.function.name}')
                rprint(f'[italic yellow]Arguments:[/italic yellow] {tool.function.arguments}')
                
                try:
                    output = function_to_call(**tool.function.arguments)
                    rprint(f'[italic yellow]Résultat de la fonction:[/italic yellow] {output}')
                except Exception as e:
                    error_msg = f"Erreur lors de l'appel de la fonction {tool.function.name}: {e}"
                    rprint(f"[bold red]Erreur[/bold red]: [underline]{error_msg}[/underline]")
                    output = error_msg
            else:
                error_msg = f"Fonction {tool.function.name} non trouvée"
                rprint(f"[bold red]Erreur[/bold red]: [underline]{error_msg}[/underline]")
                output = error_msg

        # Add the function response to messages for the model to use
        messages.append(response.message)
        
        if output is not None:
            messages.append({'role': 'tool', 'content': str(output), 'name': tool.function.name})

            # Get final response from model with function outputs
            try:
                final_response = chat(model, messages=messages, options=options)
                # rprint('[italic yellow]Réponse finale:[/italic yellow]', final_response.message.content)
            except Exception as e:
                rprint(f"[bold red]Erreur[/bold red]: [underline]Lors de la génération de la réponse finale[/underline]: {e}")
                return f"Erreur lors de la génération de la réponse finale: {e}"
        else:
            rprint('[italic yellow]Aucun résultat d\'outil à traiter[/italic yellow]')
    else:
        rprint('[italic yellow]Aucun appel d\'outil retourné par le modèle[/italic yellow]')
        

    return final_response.message.content


def ask_agent(
    prompt: Optional[str] = None,
    chron_description: Optional[str] = None,
    execute: Optional[str] = None,
    model: Optional[str] = "qwen2.5:0.5b",
    ollama_base_url: Optional[str] = "http://localhost:11434"
) -> str:
    """
    Ask the agent
    """
    # Message système avec instructions détaillées
    system_message = """Agissez en tant qu'expert en configuration de tâches cron. Votre mission est de générer une ligne de configuration crontask correctement formatée.

FORMAT STRICT À RESPECTER:
```
Minute Hour Day Month Weekday command_to_be_executed
```

RÈGLES IMPORTANTES:
1. Minute: 0-59 ou * (tous)
2. Hour: 0-23 ou * (tous)
3. Day: 1-31 ou * (tous)
4. Month: 1-12 ou * (tous)
5. Weekday: 0-6 (0=dimanche) ou * (tous)

OPÉRATEURS DISPONIBLES:
- * : tous (ex: * * * * * = chaque minute)
- , : liste de valeurs (ex: 1,3,5)
- - : plage de valeurs (ex: 1-5)
- / : pas d'incrémentation (ex: */5 = tous les 5)

CHAÎNES SPÉCIALES:
- @reboot : au démarrage
- @yearly/@annually : 0 0 1 1 * (1er janvier à minuit)
- @monthly : 0 0 1 * * (1er du mois à minuit)
- @weekly : 0 0 * * 0 (dimanche à minuit)
- @daily/@midnight : 0 0 * * * (chaque jour à minuit)
- @hourly : 0 * * * * (au début de chaque heure)

EXEMPLES CORRECTS:
- 0 7 * * * /bin/bash /opt/script.sh (tous les jours à 7h00)
- */15 * * * * /usr/bin/php /var/www/cron.php (toutes les 15 minutes)
- 0 0 * * 0 /home/user/backup.sh (chaque dimanche à minuit)
- 30 4 1,15 * * /scripts/rapport.py (les 1er et 15 du mois à 4h30)

Utilisez UNIQUEMENT la fonction write_formatted_crontask pour générer la ligne cron finale avec les paramètres exacts.
Ne répondez pas à la question, ne faite aucun commentaire, juste générez la ligne cron."""

    # Construire le message utilisateur en fonction des paramètres
    user_message = prompt if prompt else "Génère une ligne de configuration cron"
    
    # Si une commande à exécuter est fournie, l'ajouter au message
    if execute:
        user_message += f" pour exécuter la commande '{execute}'"
    else:
        # Message par défaut si aucune commande n'est spécifiée
        user_message += " pour exécuter une commande"

    if isinstance(chron_description, str):
        user_message += f"\n\nDescription de temporelle de la tâche cron: {chron_description}"

    messages_list = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
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
        model=model,
        messages=messages_list,
        tools=tools_list,
        available_functions=available_functions,
        options=mes_options,
        prompt=prompt_,
    )

    return response