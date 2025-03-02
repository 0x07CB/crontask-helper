#coding: utf-8

# Tools can still be manually defined and passed into chat
write_formatted_crontask_tool = {
    'type': 'function',
    'function': {
        'name': 'write_formatted_crontask',
        'description': 'Écrit la tâche cron formatée en combinant les champs Minute, Hour, Day, Month, Weekday et la commande à exécuter.',
        'parameters': {
            'type': 'object',
            'required': ['Minute', 'Hour', 'Day', 'Month', 'Weekday', 'command_to_be_executed'],
            'properties': {
                'Minute': {
                    'type': 'string',
                    'description': 'La minute d\'exécution (peut être un entier ou "*").'
                },
                'Hour': {
                    'type': 'string',
                    'description': 'L\'heure d\'exécution (peut être un entier ou "*").'
                },
                'Day': {
                    'type': 'string',
                    'description': 'Le jour du mois (peut être un entier ou "*").'
                },
                'Month': {
                    'type': 'string',
                    'description': 'Le mois (peut être un entier ou "*").'
                },
                'Weekday': {
                    'type': 'string',
                    'description': 'Le jour de la semaine (peut être un entier ou "*").'
                },
                'command_to_be_executed': {
                    'type': 'string',
                    'description': 'La commande à exécuter.'
                },
            },
        },
    },
}
