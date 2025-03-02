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
                    'description': 'La minute d\'exécution (0-59, *, */n, n-m, n,m,p). Exemples: "0", "*/5", "0,30", "15-45".'
                },
                'Hour': {
                    'type': 'string',
                    'description': 'L\'heure d\'exécution (0-23, *, */n, n-m, n,m,p). Exemples: "0", "*/2", "9-17", "8,12,18".'
                },
                'Day': {
                    'type': 'string',
                    'description': 'Le jour du mois (1-31, *, */n, n-m, n,m,p). Exemples: "1", "*/5", "1,15", "10-20".'
                },
                'Month': {
                    'type': 'string',
                    'description': 'Le mois (1-12, *, */n, n-m, n,m,p). Exemples: "1", "*/3", "1,6,12", "3-8".'
                },
                'Weekday': {
                    'type': 'string',
                    'description': 'Le jour de la semaine (0-6 où 0=dimanche, *, */n, n-m, n,m,p). Exemples: "0", "1-5", "0,6", "*/2".'
                },
                'command_to_be_executed': {
                    'type': 'string',
                    'description': 'La commande complète à exécuter, avec son chemin absolu et ses arguments.'
                },
            },
        },
    },
}
