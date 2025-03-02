# crontask-helper
> a crontask configuration helper ( local ollama LLM agent exemple )

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/cc070a3e4f7d410da70e3ea13d49b179)](https://app.codacy.com/gh/0x07CB/crontask-helper/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

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

Le script `main.py` constitue l'interface principale pour interagir avec l'agent de configuration de tâches cron. Il utilise la gestion d'arguments via argparse pour définir son comportement. Voici les options disponibles :

*   `-p` ou `--prompt` : Instruction destinée à l'agent, par exemple "Génère une ligne de configuration cron". Cet argument spécifie la description en langage naturel de la tâche cron à générer.
*   `-c` ou `--chronos-description` : Description temporelle de la tâche cron, par exemple "tous les jours à 7h". Cela permet de définir la planification de l'exécution.
*   `-e` ou `--execute` : Commande à exécuter par la tâche cron, telle que `/bin/bash /opt/script.sh`. Si cet argument est omis, l'agent utilisera une commande par défaut ou sollicitera des précisions supplémentaires.
*   `-m` ou `--model` : Nom du modèle Ollama à utiliser pour générer la configuration cron (défaut : `qwen2.5:0.5b`). Veillez à ce que ce modèle soit installé localement via Ollama.
*   `-u` ou `--ollama_base_url` : URL de base du serveur Ollama (défaut : `http://localhost:11434`). Modifiez ce paramètre si votre serveur Ollama est accessible à une autre adresse.
*   `-U` ou `--unload` : Flag indiquant que le modèle doit être déchargé de la mémoire après l'exécution du script, ce qui permet d'économiser des ressources système.

Pour plus de détails sur ces arguments, consultez la section d'argparsing dans le fichier `main.py`.

Voici quelques exemples d'utilisation pour illustrer comment configurer différentes tâches cron :

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
