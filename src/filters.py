import re
from typing import List, Optional

from structures import FoundSegment


class UnitFilter:
    def filter(self, line_number: int, line: Optional[str]) -> List[FoundSegment]:
        return [FoundSegment(line_number,0,line)]

def CodeBlockFilterFactory(give_in_block: bool):
    class CodeBlockFilter:
        def __init__(self):
            self.in_code_block = False
        def filter(self, line_number: int, line: Optional[str]) -> List[FoundSegment]:
            if line is None:
                return []

            if line == "```":
                self.in_code_block = not self.in_code_block
                return []
            if self.in_code_block == give_in_block:
                return [FoundSegment(line_number,0,line)] # If the line is (or is out of) a code block, return an array with a single line
            else:
                return []
    return CodeBlockFilter

def HeadingFilterFactory(heading_level: int):
    class Heading:
        def __init__(self):
            self.codeblockfilter = CodeBlockFilterFactory(False)()
        def filter(self, line_number: int, line: Optional[str]) -> List[FoundSegment]:
            codeblock_segments = self.codeblockfilter.filter(line_number, line)
            if len(codeblock_segments) != 1: # There should only be one segment (a whole line) if there is a match
                return []
                
            line_segment = codeblock_segments[0]

            count = 0
            while line_segment.text[count] == "#":
                count += 1
            valid = (heading_level != 0 and count == heading_level) or (heading_level == 0 and count != 0)

            return [FoundSegment(line_number, 0, line)] if valid else [] # headers take up the full line no matter what

    return Heading

# UnderHeadingFilter
# Keeps track of which heading level it is under to see whether to keep a line

# link_printer is a function which will format the link for printing
# TODO: There is a bug in this function, where it will claim the position as the position of the LINK, not the match.
def LinkFilterFactory(link_printer):
    link_regex = re.compile(r'\[([^\]]*)\]\(([^\]]*)\)')
    class LinkFilter:
        def __init__(self):
            self.codeblockfilter = CodeBlockFilterFactory(False)()
        def filter(self, line_number: int, line:str) -> List[FoundSegment]:
            codeblock_segments = self.codeblockfilter.filter(line_number, line)
            if len(codeblock_segments) != 1: # There should only be one segment (a whole line) if there is a match
                return []
                
            line = codeblock_segments[0]
            
            result = [] 
            for match in link_regex.finditer(line.text):
                if not match is None:
                    link_text = link_printer(match.groups()) # TODO: Reimplement link printer
                    link_position = match.start()
                    result.append(FoundSegment(line_number, link_position, link_text))

            return result
    return LinkFilter

# BoldFilter

# ItalicFilter

# Filters related to tables

# ul>li

# ol>li

# todo item

# Checked todo item

# Unchecked todo item

all = {
    'all': UnitFilter,
    'headings': HeadingFilterFactory(0),
    'heading1': HeadingFilterFactory(1),
    'heading2': HeadingFilterFactory(2),
    'heading3': HeadingFilterFactory(3),
    'heading4': HeadingFilterFactory(4),
    'heading5': HeadingFilterFactory(5),
    'heading6': HeadingFilterFactory(6),
    'links': LinkFilterFactory(lambda link: "[" + link[0] + "]" + "(" + link[1] + ")"),
    'linktarget': LinkFilterFactory(lambda link: link[0]),
    'linktext': LinkFilterFactory(lambda link: link[1]),
    'insidecodeblock': CodeBlockFilterFactory(True),
    'outsidecodeblock': CodeBlockFilterFactory(False),
}
