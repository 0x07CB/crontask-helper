# crontask-helper
> a crontask configuration helper ( local ollama LLM agent exemple )


## Introduction
Ce projet vise à simplifier la création et la gestion des tâches cron à l'aide d'un agent LLM (Large Language Model) local alimenté par Ollama. Il permet de traduire des descriptions en langage naturel en configurations de tâches cron formatées, facilitant ainsi l'automatisation des tâches planifiées sur les systèmes Unix.

## Prérequis

Avant d'utiliser `crontask-helper`, assurez-vous d'avoir les éléments suivants installés :

*   **Python 3.6+**
*   **Ollama**: Suivez les instructions d'installation sur le [site officiel d'Ollama](https://ollama.com/).
*   **Les dépendances Python**: Installez les dépendances en utilisant `pip install -r requirements.txt`.

## Installation

1.  Clonez le dépôt :

    ```bash
    git clone https://github.com/user/crontask-helper.git
    cd crontask-helper
    ```
2.  Installez les dépendances :

    ```bash
    pip install -r requirements.txt
    ```

## Utilisation

Le script principal `main.py` prend plusieurs arguments en ligne de commande :

*   `-p` ou `--prompt`: Description en langage naturel de la tâche cron à créer.
*   `-e` ou `--execute`: Commande à exécuter (optionnel, peut être inclus dans le prompt).
*   `-m` ou `--model`: Modèle Ollama à utiliser (par défaut : `qwen2.5:0.5b`).
*   `-u` ou `--ollama_base_url`: URL de base d'Ollama (par défaut : `http://localhost:11434`).
*   `-U` ou `--unload`: Décharger le modèle après l'exécution du script.

Exemple d'utilisation :