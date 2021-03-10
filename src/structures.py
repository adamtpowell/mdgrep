from typing import NamedTuple

# Holds a line and its number in the original file (used for returnarea expansion)
class FileLine(NamedTuple):
    line_number: int
    line_text: str
    
class FoundSegment(NamedTuple):
    line_number: int
    line_position: int
    text: str
    
class Expansion(NamedTuple):
    line_number: int
    line_position: int
    text: str