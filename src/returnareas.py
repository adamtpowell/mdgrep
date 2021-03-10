from typing import List
from structures import Expansion, FoundSegment

def LineArea(match: FoundSegment, filelines: List[str]) -> Expansion:
    return Expansion(match.line_number, 0, filelines[match.line_number])

def StructureArea(match: FoundSegment, filelines: List[str]) -> Expansion:
    return Expansion(match.line_number, match.line_position, match.text)

all = {
    'line': LineArea,
    'structure': StructureArea,
}