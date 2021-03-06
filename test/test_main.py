from dataclasses import dataclass
import main

# argparse generates a class-like object, not a dict-like object, so mock it with a dataclass
@dataclass
class Args:
    searcharea: str
    regex: str


def test_headings_and_grep_trivial():
    grepped_segments = main.main(Args("headings", "cat"),[
        "# heading 1",
        "# heading cat"
    ])
    assert grepped_segments[0].text == "# heading cat"

def test_headings_in_codeblock():
    greppedlines = main.main(Args("headings", None),[
        "# heading 1",
        "```",
        "# heading in code block",
        "```",
        "## heading 2",
    ])
    assert len(greppedlines) == 2
    assert greppedlines[0].text == "# heading 1"
    assert greppedlines[1].text == "## heading 2", "Heading in code block should be ignored"

# The problem with this test is that each seperate object does not get grepped
# As it stands, the entire line gets grepped, while it should be split up, in this case,
# by link.
def test_links_and_grep_trivial():
    greppedlines = main.main(Args("links", "cat|dog"),[
        "# Heading 1",
        "[https://cat.cat](Wow I like felines)",
        "# Heading 2",
        "[https://dog.dog](Wow I like canines)notalink[https://reptiles.reptiles](wow lizards amiright)",
    ])
    assert len(greppedlines) == 2
    assert greppedlines[0].text == "[https://cat.cat](Wow I like felines)"
    assert greppedlines[1].text == "[https://dog.dog](Wow I like canines)"

