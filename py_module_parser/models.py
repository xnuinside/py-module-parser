from typing import Dict, List, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field
import json


OUTPUT_TYPE = List[
    Union[
        "VariableOutput",
        "FunctionOutput",
        "CallOutput",
        "ClassOutput",
        "FromImportOutput",
    ]
]


class NodesTypes(str, Enum):
    VARIABLE = "variable"
    CALL = "call"
    CLASS = "class"
    FUNCTION_DEF = "func_def"
    IMPORT = "import"
    IMPORT_FROM = "import_from"


class ParserOutput(BaseModel):
    lineno_start: int
    lineno_end: int


class CallOutput(ParserOutput):
    """method to parse constractions like this
    `datetime.datetime.now(abc, lucky=abc, lucky2=abs)`"""

    call_name: str
    args: Optional[List]
    kwargs: Optional[Dict]
    node_type: str = NodesTypes.CALL.value


class VariableOutput(ParserOutput):
    """attribute (column) properties"""

    name: str
    # column type - varchar, double, json, etc
    # type can be dict for example: {'Union': ['dict', 'list']}
    type_annotation: Union[Dict[str, List], str, None]
    default: Optional[Union[str, int, CallOutput, list, dict]]
    node_type: str = NodesTypes.VARIABLE.value


class NameOutput(BaseModel):
    # for decorators
    # if it is decorator like @decor with out args
    # if there is and args - it will be a call
    name: str


class ClassOutput(ParserOutput):
    name: str
    parents: List[str] = Field(default_factory=list)
    attrs: List[VariableOutput] = Field(default_factory=list)
    node_type: str = NodesTypes.CLASS.value
    # nested_classes: Optional[List['ClassOutput']]


class FunctionOutput(ParserOutput):
    name: str
    parents: List[str] = Field(default_factory=list)
    node_type: str = NodesTypes.FUNCTION_DEF.value
    decorators: List[Union[CallOutput, NameOutput]]
    body: Optional[OUTPUT_TYPE]
    return_nodes: Optional[OUTPUT_TYPE]
    arguments: Optional[List[VariableOutput]]


class ImportOutput(ParserOutput):
    name: str
    alias: Optional[str]
    node_type: str = NodesTypes.IMPORT.value


class FromImportOutput(ParserOutput):
    module: str
    imports: List[ImportOutput]
    node_type: str = NodesTypes.IMPORT_FROM.value


class GroupNodesByType(BaseModel):
    imports: Optional[List[Union[ImportOutput, FromImportOutput]]]
    functions: Optional[List[FunctionOutput]]
    classes: Optional[List[ClassOutput]]
    variables: Optional[List[VariableOutput]]
    calls: Optional[List[CallOutput]]


class ParserOutput(list):
    def group_by_type(self):
        imports = []
        classes = []
        functions = []
        calls = []
        variables = []
        for node_out in self:
            node_type = node_out.node_type
            if node_type in [NodesTypes.IMPORT.value, NodesTypes.IMPORT_FROM.value]:
                imports.append(node_out)
            elif node_type == NodesTypes.CLASS.value:
                classes.append(node_out)
            elif node_type == NodesTypes.FUNCTION_DEF.value:
                functions.append(node_out)
            elif node_type == NodesTypes.CALL.value:
                calls.append(node_out)
            elif node_type == NodesTypes.VARIABLE.value:
                variables.append(node_out)
        return GroupNodesByType(
            variables=variables,
            calls=calls,
            classes=classes,
            functions=functions,
            imports=imports,
        )

    def json(self):
        if isinstance(self, list):
            _output = [i.dict() for i in self]
            return json.dumps(_output)
        else:
            return self.json()
