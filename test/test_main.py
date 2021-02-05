from dataclasses import dataclass
import main

# argparse generates a class-like object, not a dict-like object, so mock it with a dataclass
@dataclass
class Args:
    searcharea: str
    regex: str


def test_headings_and_grep_trivial():
    greppedlines = main.main(Args("headings", "cat"),[
        "# heading 1",
        "# heading cat"
    ])
    assert greppedlines[0].line_text == "# heading cat"

def test_headings_in_codeblock():
    greppedlines = main.main(Args("headings", None),[
        "# heading 1",
        "```",
        "# heading in code block",
        "```",
        "## heading 2",
    ])
    assert greppedlines[0].line_text == "# heading 1"
    assert greppedlines[1].line_text == "## heading 2", "Heading in code block should be ignored"
