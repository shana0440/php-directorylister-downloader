# below import is for self reference
from __future__ import annotations
from typing import List
from dataclasses import dataclass

@dataclass
class Link():
  name: str
  url: str
  is_folder: bool
  children: List[Link]