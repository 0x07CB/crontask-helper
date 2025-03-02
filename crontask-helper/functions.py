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
    Minute: Optional[str] = None,
    Hour: Optional[str] = None,
    Day: Optional[str] = None,
    Month: Optional[str] = None,
    Weekday: Optional[str] = None,
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
    'Minute': '*' if not isinstance(Minute, str) or len(Minute) < 1 else Minute,
    'Hour': '*' if not isinstance(Hour, str) or len(Hour) < 1 else Hour,
    'Day': '*' if not isinstance(Day, str) or len(Day) < 1 else Day,
    'Month': '*' if not isinstance(Month, str) or len(Month) < 1 else Month,
    'Weekday': '*' if not isinstance(Weekday, str) or len(Weekday) < 1 else Weekday,
    'command_to_be_executed': command_to_be_executed
  }
  
  return f"{Minute} {Hour} {Day} {Month} {Weekday} {command_to_be_executed}"

