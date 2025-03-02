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

```bash
# Générer une tâche cron pour exécuter un script tous les jours à 7h
python main.py -p "tous les jours à 7h du matin" -e "/bin/bash /opt/scripts/backup.sh"

# Générer une tâche cron pour exécuter un script toutes les 15 minutes
python main.py -p "toutes les 15 minutes" -e "/usr/bin/php /var/www/cron.php"

# Générer une tâche cron pour exécuter un script le premier jour de chaque mois à minuit
python main.py -p "le premier jour de chaque mois à minuit" -e "/home/user/monthly-report.sh"

# Utiliser un modèle différent
python main.py -p "tous les lundis à 8h" -e "/bin/bash /opt/scripts/weekly.sh" -m "llama3:8b"

# Décharger le modèle après utilisation
python main.py -p "tous les jours à 23h" -e "/bin/bash /opt/scripts/daily.sh" -U
```

## Format des tâches cron

Les tâches cron suivent un format standard avec 5 champs temporels suivis de la commande à exécuter :

```
Minute Heure JourDuMois Mois JourDeLaSemaine Commande
```

Chaque champ peut contenir :
- Des valeurs numériques spécifiques (0-59 pour les minutes, 0-23 pour les heures, etc.)
- Un astérisque (*) pour indiquer "tous"
- Des listes de valeurs séparées par des virgules (1,3,5)
- Des plages de valeurs avec un tiret (1-5)
- Des pas d'incrémentation avec une barre oblique (*/5 = tous les 5)

Exemples de formats courants :
- `0 7 * * *` : Tous les jours à 7h00
- `*/15 * * * *` : Toutes les 15 minutes
- `0 0 1 * *` : Le premier jour de chaque mois à minuit
- `0 0 * * 0` : Tous les dimanches à minuit

## Dépannage

Si vous rencontrez des problèmes :

1. Assurez-vous qu'Ollama est en cours d'exécution : `curl http://localhost:11434/api/tags`
2. Vérifiez que le modèle spécifié est disponible : `ollama list`
3. Si le modèle n'est pas disponible, téléchargez-le : `ollama pull qwen2.5:0.5b`

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.