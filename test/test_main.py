from dataclasses import dataclass
from structures import Expansion
import main

# argparse generates a class-like object, not a dict-like object, so mock it with a dataclass
@dataclass
class Args:
    searcharea: str
    regex: str
    returnarea: str

def test_unit_filter():
    grepped_segments = main.main(Args("all", None, "structure"),[
        "Line 1",
        "Line 2",
    ])
    assert sorted(grepped_segments) == sorted([
        Expansion(0, 0, "Line 1"),
        Expansion(1, 0, "Line 2"),
    ])

def test_headings_and_grep():
    grepped_segments = main.main(Args("headings", "cat", "structure"),[
        "# heading 1",
        "# heading cat"
    ])
    assert grepped_segments[0].text == "# heading cat"

def test_headings_in_codeblock():
    greppedlines = main.main(Args("headings", None, "structure"),[
        "# heading 1",
        "```",
        "# heading in code block",
        "```",
        "## heading 2",
    ])
    assert sorted(greppedlines) == sorted([
        Expansion(0, 0, "# heading 1"),
        Expansion(4, 0, "## heading 2"),
    ])

def test_headings_by_level():
    for i in range(1,7):
        grepped_lines = main.main(Args(f"heading{i}", None, "structure"),[
            "# Heading 1",
            "## Heading 2",
            "Some text",
            "### Heading 3",
            "#### Heading 4",
            "##### Heading 5",
            "fakeheading #### Heading 4",
            "###### Heading 6",
        ])
        assert len(grepped_lines) == 1
        assert grepped_lines[0].text == ("#" * i) + f" Heading {i}"

def test_links_and_grep():
    greppedlines = main.main(Args("links", "cat|dog", "structure"),[
        "# Heading 1",
        "[https://cat.cat](Wow I like felines)",
        "# Heading 2",
        "[https://dog.dog](Wow I like canines)notalink[https://reptiles.reptiles](wow lizards amiright)",
    ])
    assert sorted(greppedlines) == sorted([
        Expansion(1, 0, "[https://cat.cat](Wow I like felines)"),
        Expansion(3, 0, "[https://dog.dog](Wow I like canines)")
    ])

def test_link_targets_and_grep():
    greppedlines = main.main(Args("linktarget", "cat|reptiles", "structure"),[
        "# Heading 1",
        "[https://cat.cat](Wow I like felines)",
        "# Heading 2",
        "[https://dog.dog](Wow I like canines)notalink[https://reptiles.reptiles](wow lizards amiright)",
    ])
    assert sorted(greppedlines) == sorted([
        Expansion(1, 0, "https://cat.cat"),
        Expansion(3, 45, "https://reptiles.reptiles"),
    ])

def test_link_text_and_grep():
    greppedlines = main.main(Args("linktext", "cat|canines|reptiles|dog", "structure"),[ # Ignore any text not in link text
        "# Heading 1",
        "[https://cat.cat](Wow I like felines)",
        "# Heading 2",
        "[https://dog.dog](Wow I like canines)notalink[https://reptiles.reptiles](wow lizards amiright)",
    ])
    assert len(greppedlines) == 1
    assert greppedlines[0].text == "Wow I like canines"
    
def test_structure_vs_line():
    text = [
        "# Heading 1",
        "[https://cat.cat](Wow I like felines) this part is after the link! [https://dog.dog](This is a second link!)"
    ]
    structure_grep = main.main(Args("links", None, "structure"), text)
    line_grep = main.main(Args("links", None, "line"), text)
    
    assert sorted(structure_grep) == sorted([
        Expansion(1, 0, "[https://cat.cat](Wow I like felines)"),
        Expansion(1, 67, "[https://dog.dog](This is a second link!)")
    ])
    assert sorted(line_grep) == sorted([ # Only returns one result, since duplicate lines
        Expansion(1, 0, "[https://cat.cat](Wow I like felines) this part is after the link! [https://dog.dog](This is a second link!)"),
    ])
    
def test_section1_full_file():
    text = [
        "# Heading 1",
        "Line 1",
        "Line 2",
        "Line 3",
        "## Heading 2",
        "line 5",
    ]
    grep = main.main(Args("all", None, "section1"), text)
    assert sorted(grep) == sorted([
        Expansion(0, 0, "\n".join(text))
    ])
    
def test_section2():
    text = [
        "# Heading 1",
        "Line 1",
        "Line 2",
        "Line 3",
        "## Heading 2",
        "line 5",
    ]
    grep = main.main(Args("all", "5", "section2"), text)
    assert sorted(grep) == sorted([
        Expansion(4, 0, "\n".join([
            "## Heading 2",
            "line 5"
        ]))
    ]) 
    
def test_section2_from_section_title():
    text = [
        "# Heading 1",
        "Line 1",
        "Line 2",
        "Line 3",
        "## Heading 2",
        "line 5",
    ]
    grep = main.main(Args("heading2", None, "section2"), text)
    assert sorted(grep) == sorted([
        Expansion(4, 0, "\n".join([
            "## Heading 2",
            "line 5"
        ]))
    ])

# TODO: This behavior of crashing is correct for now, but this should fail silently and return nothing instead of crashing the program
def test_getting_section_from_outside_section_fails():
    text = [
        "# Heading 1",
        "Line 1",
        "Line 2",
        "Line 3",
        "## Heading 2",
        "line 5",
    ]
    try:
        main.main(Args("heading1", None, "section2"), text)
    except Exception as e:
        assert str(e) == "Heading of level 2 not found!"
    else:
        assert False, "Call to main.main should have failed"