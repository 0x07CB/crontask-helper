#coding: utf-8

#from datetime import datetime

#from typing import List
#from typing import Dict
#from typing import Union
#from typing import Tuple
from typing import Optional
#from typing import Any

#################
### Fonctions ###
#################

class CrontaskFormats:
  Operators = ["*", ",", "-", "/"]
  SpecialStrings = ["@reboot", "@hourly", "@daily", "@midnight", "@weekly", "@monthly", "@yearly"]

def write_formatted_crontask(
    Minute: Optional[str] = "*",
    Hour: Optional[str] = "*",
    Day: Optional[str] = "*",
    Month: Optional[str] = "*",
    Weekday: Optional[str] = "*",
    command_to_be_executed: Optional[str] = "{{command}}"
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
  # Convertir tous les arguments en chaînes de caractères et remplacer les valeurs vides ou None par '*'
  params = {
    'Minute': '*' if isinstance(Minute, None) else Minute,
    'Hour': '*' if isinstance(Hour, None) else Hour,
    'Day': '*' if isinstance(Day, None) else Day,
    'Month': '*' if isinstance(Month, None) else Month,
    'Weekday': '*' if isinstance(Weekday, None) else Weekday,
    'command_to_be_executed': command_to_be_executed
  }
  
  return f"{Minute} {Hour} {Day} {Month} {Weekday} {command_to_be_executed}"

