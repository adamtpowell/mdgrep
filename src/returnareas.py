from typing import List
from structures import Expansion, FoundSegment

def line_expansion(match: FoundSegment, filelines: List[str]) -> Expansion:
    return Expansion(match.line_number, 0, filelines[match.line_number])

def structure_expansion(match: FoundSegment, filelines: List[str]) -> Expansion:
    return Expansion(match.line_number, match.line_position, match.text)

def under_heading_expansion_factory(heading_level: int):
    def get_heading_level(line_number: int, filelines: List[str]):
        count = 0
        while count < len(filelines[line_number]) and filelines[line_number][count] == "#":
            count += 1
        return count if count != 0 else False # Return a falsy value if there is no heading, otherwise the heading level

    def under_heading_expansion(match: FoundSegment, filelines: List[str]) -> Expansion:
        # Move up to the closet instance of the given heading level
        line_number = match.line_number
        while get_heading_level(line_number, filelines) != heading_level and line_number != 0:
            line_number -= 1
            
        if line_number == 0 and get_heading_level(line_number, filelines) != heading_level:
            raise ValueError(f"Heading of level {heading_level} not found!")

        starting_line = line_number
        
        return_lines = []
        return_lines.append(filelines[line_number]) # The current line (a heading or the first line of the file) is always added
        line_number += 1

        while line_number < len(filelines) and (get_heading_level(line_number, filelines) or heading_level) >= heading_level:
            return_lines.append(filelines[line_number])
            line_number += 1
            
        return Expansion(starting_line, 0, "\n".join(return_lines))

    return under_heading_expansion

all = {
    'line': line_expansion,
    'structure': structure_expansion,
    'section1': under_heading_expansion_factory(1),
    'section2': under_heading_expansion_factory(2),
    'section3': under_heading_expansion_factory(3),
    'section4': under_heading_expansion_factory(4),
    'section5': under_heading_expansion_factory(5),
    'section6': under_heading_expansion_factory(6),
}

# Expansions TODO:
# * Codeblock
# * File
# * Table
# * List item (with subitems)