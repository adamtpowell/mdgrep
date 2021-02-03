# mdgrep
# markdown aware grep

import argparse
import functools
from typing import NamedTuple, List
import filters
import re
import sys

# Holds a line and its number in the original file (used for returnarea expansion)
class FileLine(NamedTuple):
    line_number: int
    line_text: str

# Get an array of FileLines which match the given searcharea
# Sections of each line which do not match the searcharea are ommited, leaving some lines incomplete.
# The returnarea expansion will use line metadate, so this will not be an issue.
def get_lines(searchareas: List[str], filelines: List[str]) -> List[FileLine]:
    # Initialize filters
    used_filters = [filters.all[area]() for area in searchareas]
    lines: List[FileLine] = []
    for line_number, line in enumerate(filelines):
        filtered_line = line.rstrip()
        for filter in used_filters:
            filtered_line = filter.filter(filtered_line)
        if not filtered_line is None: lines.append(FileLine(line_number, filtered_line))
    return lines

def render_file_lines(filelines: List[FileLine]):
    result = ""
    for fileline in filelines:
        result += str(fileline.line_number) + " " + fileline.line_text + "\n"
    return result

def main(args):
    # Get the text to search for based on args.searcharea
    filelines = sys.stdin.readlines()
    print(filelines)
    lines = get_lines(args.searcharea.split(','), filelines)

    # Use grep
    if not args.regex is None:
        grepped_lines = []
        for line in lines:
            line_matches = re.findall(args.regex, line.line_text) 
            if len(line_matches) != 0:
                grepped_lines.append(line)
    else:
        grepped_lines = lines

    # Expand to args.returnarea

    print(render_file_lines(grepped_lines), end='')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Markdown aware grep')
    parser.add_argument(
            '--regex',
            required=False,
            help='The regex to use'
    )
    parser.add_argument(
            '--searcharea',
            default='all',
            help='The area(s) in which to search. Includes: all,headings'
    )
    args = parser.parse_args()

    main(args)
