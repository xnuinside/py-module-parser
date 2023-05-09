from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class ParserOutput(BaseModel):
    lineno_start: int
    lineno_end: int


class FuncCallOutput(ParserOutput):
    """method to parse constractions like this
    `datetime.datetime.now(abc, lucky=abc, lucky2=abs)`"""

    func_name: str
    args: Optional[List]
    kwargs: Optional[Dict]
    node_type: str = "func_call"


class VariableOutput(ParserOutput):
    """attribute (column) properties"""

    name: str
    # column type - varchar, double, json, etc
    # type can be dict for example: {'Union': ['dict', 'list']}
    type_annotation: Union[Dict[str, List], str, None]
    default: Optional[Union[str, int, FuncCallOutput, list, dict]]
    properties: Dict[str, Any] = Field(default_factory=dict)
    node_type: str = "variable"


class ClassOutput(ParserOutput):
    name: str
    parents: List[str] = Field(default_factory=list)
    attrs: List[VariableOutput] = Field(default_factory=list)
    node_type: str = "class"


class ImportOutput(ParserOutput):
    name: str
    alias: Optional[str]
    node_type: str = "import"


class FromImportOutput(ParserOutput):
    module: str
    imports: List[ImportOutput]
    node_type: str = "from_import"
