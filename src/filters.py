from typing import Optional
import re

class UnitFilter:
    def filter(self, line: str):
        return line

def HeadingFilterFactory(heading_level: int):
    class Heading:
        def filter(self, line: str) -> Optional[str]:
            if len(line) == 0:
                return None

            count = 0
            while line[count] == "#":
                count += 1
            valid = (heading_level != 0 and count == heading_level) or (heading_level == 0 and count != 0)

            return line if valid else None

    return Heading

# UnderHeadingFilter
# Keeps track of which heading level it is under to see whether to keep a line

def LinkFilterFactory(link_printer):
    link_regex = re.compile(r'\[([^\]]*)\]\(([^\]]*)\)')
    class LinkFilter:
        def filter(self, line:str):
           result = ""
           links = link_regex.findall(line) 
           for link in links:
               if not link is None:
                   result += link_printer(link)
           return result if result != "" else None
    return LinkFilter

# BoldFilter

# ItalicFilter

all = {
    'all': UnitFilter,
    'headings': HeadingFilterFactory(0),
    'heading1': HeadingFilterFactory(1),
    'heading2': HeadingFilterFactory(2),
    'heading3': HeadingFilterFactory(3),
    'heading4': HeadingFilterFactory(4),
    'heading5': HeadingFilterFactory(5),
    'heading6': HeadingFilterFactory(6),
    'link': LinkFilterFactory(lambda link: "[" + link[0] + "]" + "(" + link[1] + ")"),
    'linktarget': LinkFilterFactory(lambda link: link[0]),
    'linktext': LinkFilterFactory(lambda link: link[1]),
}
