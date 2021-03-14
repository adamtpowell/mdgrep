# mdgrep

A markdown aware searching tool.

Works in three steps:
1. Filtering; filter the markdown file for just the items you want (a specific heading level, link text, unfilled todo items, etc.)
2. Grepping; use a regex to search through each filtered section.
3. Expansion; expanding from each grepped match to a given area (could be the whole line, the link the match is from, the current section of the file, etc.)

## Why

To make it easy to write ad-hoc syntax for adding functionality and interacting with markdown-based wikis. It may also be useful for things like literate programming, static site generation, etc. 

The main improvements over just grepping for lines is the ability to pull out sections of the document, ignore lines that fall inside codeblocks, and saving time when writing regexes to filter for certain features in the markdown.

The design aims to be faster (but less correct) than parsing the markdown fully.
