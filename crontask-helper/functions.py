#coding: utf-8

#from datetime import datetime

#from typing import List
#from typing import Dict
from typing import Union
#from typing import Tuple
#from typing import Optional
#from typing import Any

#################
### Fonctions ###
#################

class CrontaskFormats:
  Operators = ["*", ",", "-", "/"]
  SpecialStrings = ["@reboot", "@hourly", "@daily", "@midnight", "@weekly", "@monthly", "@yearly"]

def write_formatted_crontask(
    Minute: Union[str, int],
    Hour: Union[str, int],
    Day: Union[str, int],
    Month: Union[str, int],
    Weekday: Union[str, int],
    command_to_be_executed: str
) -> str:
  """
  Write the formatted crontask with validation of input parameters
  
  Args:
      Minute: Minute of execution
      Hour: Hour of execution
      Day: Day of month
      Month: Month of execution
      Weekday: Day of week
      command_to_be_executed: Command to be executed
  
  Raises:
      ValueError: If any parameter is None, empty, or contains only whitespace
  """
  # Convertir tous les arguments en chaînes de caractères
  params = {
    'Minute': str(Minute),
    'Hour': str(Hour),
    'Day': str(Day),
    'Month': str(Month),
    'Weekday': str(Weekday),
    'command_to_be_executed': command_to_be_executed
  }
  
  # Vérifier que chaque paramètre est renseigné et non vide
  for param_name, param_value in params.items():
    if param_value is None or param_value.strip() == '':
      raise ValueError(f"Le paramètre {param_name} ne peut pas être vide ou None")
  
  return f"{Minute} {Hour} {Day} {Month} {Weekday} {command_to_be_executed}"

