#!/usr/bin/env python3
#coding: utf-8

__version__ = "0.1.1"
__author__ = "@0x07cb"
__description__ = "Assistant pour générer des tâches cron"

from bdb import effective
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

    Cette fonction effective les étapes suivantes :
    1. Vérifie la connectivité avec le serveur Ollama
    2. Appelle l'agent pour générer une configuration de tâche cron
    3. Affiche le résultat final
    4. Gère les erreurs et interruptions
    5. Décharge optionnellement le modèle de la mémoire

    Args:
        prompt (Optional[str]): Instruction pour l'agent, décrivant la tâche cron à générer
        chron_description (Optional[str]): Description temporelle de la tâche cron 
        execute (Optional[str]): Commande spécifique à exécuter dans la tâche cron
        model (Optional[str]): Modèle Ollama à utiliser pour la génération (défaut: "llama3.2:3b")
        ollama_base_url (Optional[str]): URL du serveur Ollama (défaut: "http://localhost:11434")
        unload (Optional[bool]): Indicateur pour décharger le modèle après utilisation

    Raises:
        requests.exceptions.RequestException: Si la connexion à Ollama échoue
        KeyboardInterrupt: Si l'utilisateur interrompt l'exécution
        Exception: Pour toute autre erreur inattendue
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


def usage():
    rprint(f"[bold cyan]Usage:[/bold cyan] [green]crontask-helper[/green] [yellow][options][/yellow]")
    rprint(f"[bold white]Options:[/bold white]")
    rprint(f"  [blue]-p[/blue], [blue]--prompt[/blue] <[magenta]prompt[/magenta]>    [white]Instruction pour l'agent[/white] [dim](ex: \"[italic]Génère une ligne de configuration cron[/italic]\")")
    rprint(f"  [blue]-c[/blue], [blue]--chronos-description[/blue] <[magenta]description[/magenta]>    [white]Description temporelle de la tâche cron[/white] [dim](ex: \"[italic]tous les jours à 7h[/italic]\")")
    rprint(f"  [blue]-e[/blue], [blue]--execute[/blue] <[magenta]commande[/magenta]>    [white]Commande à exécuter dans la tâche cron[/white] [dim](ex: \"[italic]/bin/bash /opt/script.sh[/italic]\")")
    rprint(f"  [blue]-m[/blue], [blue]--model[/blue] <[magenta]model[/magenta]>    [white]Modèle Ollama à utiliser[/white] [dim](défaut: [italic]llama3.2:3b[/italic])")
    rprint(f"  [blue]-u[/blue], [blue]--ollama-base-url[/blue] <[magenta]url[/magenta]>    [white]URL de base du serveur Ollama[/white] [dim](défaut: [italic]http://localhost:11434[/italic])")
    rprint(f"  [blue]-U[/blue], [blue]--unload[/blue]    [white]Décharger le modèle après utilisation[/white]")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(prog=f"crontask-helper v{__version__}",
                                     description='CronTask Helper - Assistant pour générer des tâches cron'
                                     )
    
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