MCQ Generator
=============

Generate multiple-choice questions (MCQs) from input text using a simple keyword-based cloze technique.

Installation (editable)
-----------------------

```bash
pip install -e .
```

Usage
-----

- From inline text:

```bash
mcqgen --text "Natural language processing enables computers to understand human language." --num 3 --choices 4
```

- From a file:

```bash
mcqgen --input-file path/to/text.txt --num 5 --choices 4
```

- Output JSON:

```bash
mcqgen --text "Large language models are trained on vast datasets." --json
```

Library API
-----------

```python
from mcqgenerator import generate_mcqs

text = "Natural language processing enables computers to understand human language."
mcqs = generate_mcqs(text, num_questions=3, num_choices=4)
```


