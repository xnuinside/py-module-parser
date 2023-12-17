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

Example with different output formats provided in example/example.py

```python
    # to run example
    python example/example.py

```

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
        node_type='import_from'
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
                value=CallOutput(
                    lineno_start=5,
                    lineno_end=5,
                    func_name='models.CharField',
                    args=[],
                    kwargs={'max_length': 50},
                    node_type='call'
                ),
                properties={},
                node_type='variable'
            ),
            VariableOutput(
                lineno_start=6,
                lineno_end=6,
                name='last_name',
                type_annotation=None,
                value=CallOutput(
                    lineno_start=6,
                    lineno_end=6,
                    func_name='models.CharField',
                    args=[],
                    kwargs={'max_length': 50},
                    node_type='call'
                ),
                properties={},
                node_type='variable'
            ),
            VariableOutput(
                lineno_start=7,
                lineno_end=7,
                name='instrument',
                type_annotation=None,
                value=CallOutput(
                    lineno_start=7,
                    lineno_end=7,
                    func_name='models.CharField',
                    args=[],
                    kwargs={'max_length': 100},
                    node_type='call'
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

## Parser Output

By default parser output is a ParserOutput model -it is a list with some additional methods.
List contains inside a nodes from parsed files - all Nodes is a Pydantic models with nested objects.

List of possible node types exists as enum in py_modules_parser.NodesTypes:
    
VARIABLE = 'variable' - all variables like `a='b'`
CALL = 'call' - all calls - function calls or class calls like `func_name(a)` or `ClassA()`
CLASS = 'class' - classes defenitions `class SomeClass: ...`
FUNCTION_DEF = 'func_def' - functions defenitions `def some_func(): ...`
IMPORT = 'import' - imports like `import module`
IMPORT_FROM = 'import_from' - imports like `from module import name`

Output is a list of pydantic models specific for each node.
Node type is always stored in argumen `node_type`

Because, output models is Pydantic models - you can do anything with them that you can do with pydantic models.

### Output group_by_type


```python

    parsed_output = PyModulesParser(source_code).parse()
    parsed_output_group = parsed_output.group_by_type()
    print("Result group_by_type: \n", parsed_output_group)
    # you can also use parsed_output.group_by_type().json()
    # to get json output grouped by type

```

### Output json

```python

parsed_output = PyModulesParser(source_code).parse()
parsed_output_json= parsed_output.json()
print("Result in json: \n", parsed_output_json)

```
### Output dict

```python

parsed_output = PyModulesParser(source_code).parse()
parsed_output_group_dict = parsed_output.group_by_type().model_dump()
print("Result as python dict: \n")
print(parsed_output_group_dict)

```


## TODO in future releases
1. Implement parsing of function arguments
2. Implement parsing of function returns
3. Implement parsing of nested classes

## Changelog
** 0.5.0 - Update pydantic to 2.x version **

1. Pydantic is updated to 2.5.2
2. VariableOutput.default was renamed to VariableOutput.value


** 0.4.0 - First stable release**

1. Renamed FuncCallOutput to CallOutput to include Class calls as well as function calls.
2. Added Enum to define available NodeTypes as py_module_parser.NodeTypes.
3. Added parsing of function definition nodes.
4. Implemented parsing of decorators.
5. Parser results can now be dumped to Python dictionaries or JSON, as well as grouped by type. For more details, please refer to the example/ directory and the README file.




