"""A class for any arbitary object being cited"""
from typing import Any, NewType

Citable = NewType("Citable", Any)
