# Python Module Parser
![badge1](https://img.shields.io/pypi/v/py-module-parser) ![badge2](https://img.shields.io/pypi/l/py-module-parser) ![badge3](https://img.shields.io/pypi/pyversions/py-module-parser)![workflow](https://github.com/xnuinside/py-module-parser/actions/workflows/main.yml/badge.svg)

Python Module Parser is a library that parses Python modules and outputs information about imports, functions, variables, and their corresponding line numbers. This makes it easier to analyze and understand the structure of your Python code.

To get more samples of output - check tests: tests/test_py_module_parser.py

This project inspired by https://github.com/xnuinside/codegraph and https://github.com/xnuinside/py-models-parser and will be used as a parser inside them in the future. 

## Features

- Parse Python modules and extract information about imports, functions, and variables
- Identify line numbers for each import, function, and variable
- Represent the extracted information in a structured format

## Installation

To install the Python Module Parser library, use `pip`:

```bash
    pip install py-module-parser
```


## Usage
Here's a simple example of how to use the Python Module Parser library:

```python
from py_module_parser import PyModulesParser

source_code = """from django.db import models


class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)

"""
parsed_output = PyModulesParser(source_code).parse()
print(parsed_output)
```

This will output:

```python
[
    FromImportOutput(
        lineno_start=1,
        lineno_end=1,
        module='django.db',
        imports=[
            ImportOutput(
                lineno_start=1,
                lineno_end=1,
                name='models',
                alias=None,
                node_type='import'
            )
        ],
        node_type='from_import'
    ),
    ClassOutput(
        lineno_start=4,
        lineno_end=7,
        name='Musician',
        parents=['models.Model'],
        attrs=[
            VariableOutput(
                lineno_start=5,
                lineno_end=5,
                name='first_name',
                type_annotation=None,
                default=FuncCallOutput(
                    lineno_start=5,
                    lineno_end=5,
                    func_name='models.CharField',
                    args=[],
                    kwargs={'max_length': 50},
                    node_type='func_call'
                ),
                properties={},
                node_type='variable'
            ),
            VariableOutput(
                lineno_start=6,
                lineno_end=6,
                name='last_name',
                type_annotation=None,
                default=FuncCallOutput(
                    lineno_start=6,
                    lineno_end=6,
                    func_name='models.CharField',
                    args=[],
                    kwargs={'max_length': 50},
                    node_type='func_call'
                ),
                properties={},
                node_type='variable'
            ),
            VariableOutput(
                lineno_start=7,
                lineno_end=7,
                name='instrument',
                type_annotation=None,
                default=FuncCallOutput(
                    lineno_start=7,
                    lineno_end=7,
                    func_name='models.CharField',
                    args=[],
                    kwargs={'max_length': 100},
                    node_type='func_call'
                ),
                properties={},
                node_type='variable'
            )
        ],
        node_type='class'
    )
]
```

To parse from file, you can use method `parse_from_file`

```python
from py_module_parser import parse_from_file

parsed_output = parse_from_file(file_path='path_to/python_module.py')
print(parsed_output)
```
