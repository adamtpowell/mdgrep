# mdgrep
# markdown aware grep

import argparse
import functools
from typing import NamedTuple, List
import filters
import re
import sys
from structures import FileLine, FoundSegment
import returnareas

# Returns all of the matches from the filter stack
# Matches from before the last filter are recombined into a line for future filters
# to work from.
def get_matches(searchareas: List[str], filelines: List[str]) -> List[FoundSegment]:
    used_filters = [filters.all[area]() for area in searchareas]
    segments: List[FoundSegment] = []

    for line_number, line in enumerate(filelines):
        filtered_line = line.rstrip()
        for i, filter in enumerate(used_filters):
            line_matches = filter.filter(line_number, filtered_line)
            assert line_matches == sorted(line_matches, key=lambda match: match.line_position), "Filters should return matches sorted by line position."
            filtered_line = "".join(match.text for match in line_matches)
            
        for match in line_matches: # Append all matches from the FINAL filter.
            segments.append(match)

    return segments

def render_file_lines(filelines: List[FileLine]):
    result = ""
    for fileline in filelines:
        result += str(fileline.line_number) + " " + fileline.line_text + "\n"
    return result

def main(args, filelines) -> List[str]:
    # apply --searchareas
    matches = get_matches(args.searcharea.split(','), filelines)

    # Apply --regex
    if args.regex is None:
        grepped_matches = matches
    else:
        grepped_matches = []
        for match in matches:
            match_grep_matches = re.findall(args.regex, match.text) 
            if len(match_grep_matches) != 0:
                grepped_matches.append(match)

    # apply --returnarea
    expansions = []
    for match in grepped_matches:
        expansion = returnareas.all[args.returnarea](match, filelines)
        if not expansion is None:
            expansions.append(expansion)

    if args.deduplicate == "true":
        return list(set(expansions))
    elif args.deduplicate == "false":
        return expansions
    else:
        raise ValueError("Invalid value for deduplicate. Please use true or false")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Markdown aware grep')
    parser.add_argument(
        '--regex',
        required=False,
        help='The regex to use'
    )
    parser.add_argument(
        '--deduplicate',
        default='true',
        help='true or false; whether to remove duplicate matches'
    )
    parser.add_argument(
        '--searcharea',
        default='all',
        help='The area(s) in which to search. Includes: all,headings'
    )
    parser.add_argument(
        '--returnarea',
        default='structure',
        help='The structure to return'
    )
    args = parser.parse_args()

    grepped_lines = main(args, sys.stdin.readlines())
    print(render_file_lines(grepped_lines), end='')