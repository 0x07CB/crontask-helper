#!/usr/bin/env python3
#coding: utf-8

#from ollama import generate
#from ollama._types import Options
#from ollama import ChatResponse
#from ollama import chat

import sys
from typing import Optional

from agents import ask_agent
from agents import model_unload

from rich import print as rprint

def main(
    prompt: Optional[str] = None,
    chron_description: Optional[str] = None,
    execute: Optional[str] = None,
    model: Optional[str] = "llama3.2:3b",
    ollama_base_url: Optional[str] = "http://localhost:11434",
    unload: Optional[bool] = False,
):
    """
    Fonction principale qui gère l'interaction avec l'agent crontask
    
    Args:
        prompt: Description de la tâche cron à générer
        execute: Commande à exécuter dans la tâche cron
        model: Modèle Ollama à utiliser
        ollama_base_url: URL de base du serveur Ollama
        unload: Si True, décharge le modèle après utilisation
    """
    try:
        # Vérifier si Ollama est accessible
        import requests
        try:
            response = requests.get(f"{ollama_base_url}/api/tags")
            if response.status_code != 200:
                rprint(f"[bold red]Erreur[/bold red]: [underline]Impossible de se connecter à Ollama sur {ollama_base_url}[/underline]")
                rprint(f"[bold white]Statut[/bold white]: [bold red]{response.status_code}[/bold red]")
                sys.exit(1)

        except requests.exceptions.RequestException as e:
            rprint(f"[bold red]Erreur[/bold red]: [underline]Impossible de se connecter à Ollama sur {ollama_base_url}[/underline]")
            rprint(f"[bold white]Exception[/bold white]: [bold red]{e}[/bold red]")
            sys.exit(1)
            
        # Appeler l'agent
        result = ask_agent(prompt,
                           chron_description,
                           execute, 
                           model, 
                           ollama_base_url)
        rprint(f"\n[bold green]Résultat final[/bold green]: {result}")
        
    except KeyboardInterrupt:
        rprint("\n[bold yellow]Interruption par l'utilisateur[/bold yellow]")
        sys.exit(0)
    except Exception as e:
        rprint(f"\n[bold red]Erreur[/bold red]: {e}")
        sys.exit(1)
    finally:
        if unload:
            try:
                rprint(f"\n[italic yellow]Déchargement du modèle {model}...[/italic yellow]")
                model_unload(model, ollama_base_url)
            except Exception as e:
                rprint(f"[bold red]Erreur[/bold red]: [underline]Lors du déchargement du modèle[/underline]: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='CronTask Helper - Assistant pour générer des tâches cron')
    parser.add_argument('-p', '--prompt', type=str, default=None, 
                        help='Instruction pour l\'agent (ex: "Génère une ligne de configuration cron")')
    parser.add_argument('-c', '--chronos-description', type=str, default=None, 
                        help='Description de temporelle de la tâche cron (ex: "tous les jours à 7h")')
    parser.add_argument('-e', '--execute', type=str, default=None, 
                        help='Commande à exécuter dans la tâche cron (ex: "/bin/bash /opt/script.sh")')
    parser.add_argument('-m', '--model', type=str, default="llama3.2:3b", 
                        help='Modèle Ollama à utiliser (défaut: llama3.2:3b)')
    parser.add_argument('-u', '--ollama-base-url', type=str, default="http://localhost:11434", 
                        help='URL de base du serveur Ollama (défaut: http://localhost:11434)')
    parser.add_argument('-U', '--unload', action='store_true', default=False, 
                        help='Décharger le modèle après utilisation')
    args = parser.parse_args()

    try:
        main(
            prompt=args.prompt,
            chron_description=args.chronos_description,
            execute=args.execute,
            model=args.model,
            ollama_base_url=args.ollama_base_url,
            unload=args.unload
        )
    except KeyboardInterrupt:
        rprint("\n[bold yellow]Programme interrompu par l'utilisateur[/bold yellow]")
        sys.exit(0)
    
    sys.exit(0)