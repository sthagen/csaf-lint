# Test Fixtures
The corpus of documents is organized per version folders.

## CSAF Version 2.0
Inside the CSAF version 2.0 folder the sub folders further split per:
1. Scope - currently `baseline` and `invalid`
2. Content - combinations of schema parts
Figure: 1 Folder tree
```
csaf-2.0/
├── baseline
│    ├── document
│    ├── document-product
│    ├── document-vulnerability
│    ├── full
│    └── spam
└── invalid
      ├── document
      ├── document-product
      ├── document-vulnerability
      ├── full
      └── spam
```
**Note**: `spam` indicates minimal valid documents because these do no convey anything meaningful on their own.

### File Name Patterns
The file names within the leaf folders match the following regular expression:
```
\d\d\.json
```
In case more than 99 distinct fixtures are present, the pattern may be augmented to align numerical with lexical ordering.
