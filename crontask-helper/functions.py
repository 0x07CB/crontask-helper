#coding: utf-8

from datetime import datetime

from typing import List
from typing import Dict
from typing import Union
from typing import Tuple
from typing import Optional
from typing import Any

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
  Write the formatted crontask
  """
  return f"{Minute} {Hour} {Day} {Month} {Weekday} {command_to_be_executed}"

