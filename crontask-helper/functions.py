#coding: utf-8

#from datetime import datetime

#from typing import List
#from typing import Dict
from typing import Union
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
    Minute: Optional[Union[str, int]] = "*",
    Hour: Optional[Union[str, int]] = "*",
    Day: Optional[Union[str, int]] = "*",
    Month: Optional[Union[str, int]] = "*",
    Weekday: Optional[Union[str, int]] = "*",
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
    'Minute': '*' if Minute is None or str(Minute).strip() == '' else str(Minute),
    'Hour': '*' if Hour is None or str(Hour).strip() == '' else str(Hour),
    'Day': '*' if Day is None or str(Day).strip() == '' else str(Day),
    'Month': '*' if Month is None or str(Month).strip() == '' else str(Month),
    'Weekday': '*' if Weekday is None or str(Weekday).strip() == '' else str(Weekday),
    'command_to_be_executed': command_to_be_executed
  }
  
  return f"{Minute} {Hour} {Day} {Month} {Weekday} {command_to_be_executed}"

