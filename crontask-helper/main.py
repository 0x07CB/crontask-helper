#!/usr/bin/env python3
#coding: utf-8

#from ollama import generate
#from ollama._types import Options
#from ollama import ChatResponse
#from ollama import chat

import sys
import os
from typing import List, Dict, Union, Tuple, Optional, Any

from agents import ask_agent
from agents import model_unload


def main(
    prompt: Optional[str] = None,
    chron_description: Optional[str] = None,
    execute: Optional[str] = None,
    model: Optional[str] = "qwen2.5:0.5b",
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
                print(f"Erreur: Impossible de se connecter à Ollama sur {ollama_base_url}")
                print(f"Statut: {response.status_code}")
                sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(f"Erreur: Impossible de se connecter à Ollama sur {ollama_base_url}")
            print(f"Exception: {e}")
            sys.exit(1)
            
        # Appeler l'agent
        result = ask_agent(prompt,
                           chron_description,
                           execute, 
                           model, 
                           ollama_base_url)
        print("\nRésultat final:")
        print(result)
        
    except KeyboardInterrupt:
        print("\nInterruption par l'utilisateur", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nErreur: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if unload:
            try:
                print(f"\nDéchargement du modèle {model}...")
                model_unload(model, ollama_base_url)
            except Exception as e:
                print(f"Erreur lors du déchargement du modèle: {e}", file=sys.stderr)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='CronTask Helper - Assistant pour générer des tâches cron')
    parser.add_argument('-p', '--prompt', type=str, default=None, 
                        help='Instruction pour l\'agent (ex: "Génère une ligne de configuration cron")')
    parser.add_argument('-c', '--chronos-description', type=str, default=None, 
                        help='Description de temporelle de la tâche cron (ex: "tous les jours à 7h")')
    parser.add_argument('-e', '--execute', type=str, default=None, 
                        help='Commande à exécuter dans la tâche cron (ex: "/bin/bash /opt/script.sh")')
    parser.add_argument('-m', '--model', type=str, default="qwen2.5:0.5b", 
                        help='Modèle Ollama à utiliser (défaut: qwen2.5:0.5b)')
    parser.add_argument('-u', '--ollama_base_url', type=str, default="http://localhost:11434", 
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
        print("\nProgramme interrompu par l'utilisateur", file=sys.stderr)
        sys.exit(1)
    
    sys.exit(0)