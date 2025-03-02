#coding: utf-8

# Tools can still be manually defined and passed into chat
write_formatted_crontask_tool = {
    'type': 'function',
    'function': {
        'name': 'write_formatted_crontask',
        'description': 'Écrit la tâche cron formatée en combinant les champs Minute, Hour, Day, Month, Weekday et la commande à exécuter. Respectez strictement le format cron standard.',
        'parameters': {
            'type': 'object',
            'required': ['Minute', 'Hour', 'Day', 'Month', 'Weekday', 'command_to_be_executed'],
            'properties': {
                'Minute': {
                    'type': 'string',
                    'minLength': 1,
                    'pattern': '^[0-9*,-/]+$',
                    'description': 'La minute d\'exécution (numéro ou expression cron utilisant des opérateurs parmi "*", "-", "/", ","). Exemples: "0", "*/5", "0,30", "15-45".'
                },
                'Hour': {
                    'type': 'string',
                    'minLength': 1,
                    'pattern': '^[0-9*,-/]+$',
                    'description': 'L\'heure d\'exécution (numéro ou expression cron utilisant des opérateurs parmi "*", "-", "/", ","). Exemples: "0", "*/2", "9-17", "8,12,18".'
                },
                'Day': {
                    'type': 'string',
                    'minLength': 1,
                    'pattern': '^[0-9*,-/]+$',
                    'description': 'Le jour du mois (numéro ou expression cron utilisant des opérateurs parmi "*", "-", "/", ","). Exemples: "1", "*/5", "1,15", "10-20".'
                },
                'Month': {
                    'type': 'string',
                    'minLength': 1,
                    'pattern': '^[0-9*,-/]+$',
                    'description': 'Le mois (numéro ou expression cron utilisant des opérateurs parmi "*", "-", "/", ","). Exemples: "1", "*/3", "1,6,12", "3-8".'
                },
                'Weekday': {
                    'type': 'string',
                    'minLength': 1,
                    'pattern': '^[0-9*,-/]+$',
                    'description': 'Le jour de la semaine (numéro ou expression cron utilisant des opérateurs parmi "*", "-", "/", ","). Exemples: "0", "1-5", "0,6", "*/2".'
                },
                'command_to_be_executed': {
                    'type': 'string',
                    'minLength': 1,
                    'description': 'La commande complète à exécuter, avec son chemin absolu et ses arguments.'
                },
            },
        },
    },
}
