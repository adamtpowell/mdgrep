from dataclasses import dataclass
import main

# argparse generates a class-like object, not a dict-like object, so mock it with a dataclass
@dataclass
class Args:
    searcharea: str
    regex: str

def test_unit_filter():
    grepped_segments = main.main(Args("all", None),[
        "Line 1",
        "Line 2",
    ])
    assert len(grepped_segments) == 2
    assert grepped_segments[0].text == "Line 1"
    assert grepped_segments[1].text == "Line 2"

def test_headings_and_grep():
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

def test_headings_by_level():
    for i in range(1,7):
        grepped_lines = main.main(Args(f"heading{i}", None),[
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
    greppedlines = main.main(Args("links", "cat|dog"),[
        "# Heading 1",
        "[https://cat.cat](Wow I like felines)",
        "# Heading 2",
        "[https://dog.dog](Wow I like canines)notalink[https://reptiles.reptiles](wow lizards amiright)",
    ])
    assert len(greppedlines) == 2
    assert greppedlines[0].text == "[https://cat.cat](Wow I like felines)"
    assert greppedlines[1].text == "[https://dog.dog](Wow I like canines)"

def test_link_targets_and_grep():
    greppedlines = main.main(Args("linktarget", "cat|dog"),[
        "# Heading 1",
        "[https://cat.cat](Wow I like felines)",
        "# Heading 2",
        "[https://dog.dog](Wow I like canines)notalink[https://reptiles.reptiles](wow lizards amiright)",
    ])
    assert len(greppedlines) == 2
    assert greppedlines[0].text == "https://cat.cat"
    assert greppedlines[1].text == "https://dog.dog"

def test_link_text_and_grep():
    greppedlines = main.main(Args("linktext", "cat|canines|reptiles|dog"),[ # Ignore any text not in link text
        "# Heading 1",
        "[https://cat.cat](Wow I like felines)",
        "# Heading 2",
        "[https://dog.dog](Wow I like canines)notalink[https://reptiles.reptiles](wow lizards amiright)",
    ])
    assert len(greppedlines) == 1
    assert greppedlines[0].text == "Wow I like canines"