# mdgrep

A markdown aware searching tool.

## Folder Structure

```
├── filters.py # Contains filters for --searcharea
├── main.py
├── readme.md
└── tests # Test code, needs bats installed to run
    ├── input.md
    └── tests.bats
```

2 directories, 6 files

## Examples

### Search through image alttext for images of cats
mdgrep 'cat' --searchfilters alttext

### Subsections which talk about cats
Returns the full text of every level (everything directly under the current heading) which uses 'cat' anywhere in the text.

cat * | mdgrep 'cat' --returnarea aroundlevel

### Print the names of every file which is not linked to TODO: Remove psuedocode
```
for file in files:
    cat * | mdgrep 'file' --searchfilters linktarget != empty
```
