import _ast
import ast
from typing import Any, Dict, List, Union

from py_module_parser.models import (
    ClassOutput,
    FromImportOutput,
    CallOutput,
    ImportOutput,
    VariableOutput,
    FunctionOutput,
    GroupNodesByType,
    NodesTypes,
    NameOutput,
    OUTPUT_TYPE,
)


class PyModulesParser:
    def __init__(self, input_code: str, group_by_type: bool = False) -> None:
        self.input_code = input_code
        self.group_by_type = group_by_type

    def process_assign_node(
        self, node: ast.Assign, _attrs: List
    ) -> List[VariableOutput]:
        _type = None
        print(node.targets[0].id)
        if isinstance(node.value, ast.Constant):
            # like a = 'b'
            value = node.value.value
            _type = type(node.value.value).__name__
        elif isinstance(node.value, _ast.Call):
            value = self.process_call_node(node.value)
            _type = None
        elif isinstance(node.value, ast.Name):
            value = node.value.id
        else:
            value = node.value.id
            raise
        for target in node.targets:
            name = target.id
            _attr = VariableOutput(
                name=name,
                default=value,
                type_annotation=_type,
                lineno_start=node.lineno,
                lineno_end=node.end_lineno,
            )
            _attrs.append(_attr)
        print(_attrs)
        return _attrs

    def process_annotation(
        self, ann: Union[ast.Name, _ast.Subscript, _ast.Attribute]
    ) -> Union[Dict, str]:
        if isinstance(ann, ast.Name):
            _type = ann.id
        elif isinstance(ann, _ast.Subscript):
            if isinstance(ann.slice.value, ast.Name):
                _type_value = [ann.slice.value.id]
            elif isinstance(ann.slice.value, ast.Attribute):
                _type_value = [self.process_full_attr_node_name(ann.slice.value, None)]
            else:
                _type_value = [name.id for name in ann.slice.value.elts]
            _type = {ann.value.id: _type_value}
        elif isinstance(ann, _ast.Attribute):
            _type = f"{ann.attr}.{ann.value.id}"
        else:
            _type = ann
        return _type

    def process_full_attr_node_name(
        self, attr_node: _ast.Attribute, previous_path: str
    ) -> str:
        if isinstance(attr_node, _ast.Attribute):
            previous_path = (
                f"{attr_node.attr}.{previous_path}" if previous_path else attr_node.attr
            )
            return self.process_full_attr_node_name(
                attr_node.value, previous_path=previous_path
            )
        elif isinstance(attr_node, _ast.Name):
            return f"{attr_node.id}.{previous_path}"

    def process_keyword(self, node) -> Dict[Any, Any]:
        key = node.arg
        if isinstance(node.value, ast.Constant):
            value = node.value.value
        else:
            if isinstance(node.value, ast.Attribute):
                value = node.value.value.id
            else:
                value = node.value.id
        return {key: value}

    def process_call_node(self, node: _ast.Call) -> CallOutput:
        if isinstance(node.func, _ast.Attribute):
            call_name = self.process_full_attr_node_name(node.func, None)
        elif isinstance(node.func, ast.Name):
            call_name = node.func.id
        kwargs = {}
        for _node in node.keywords:
            kwargs.update(self.process_keyword(_node))

        args = []

        for _node in node.args:
            if isinstance(_node, ast.Attribute):
                arg = _node.value.id
            elif isinstance(_node, ast.Call):
                arg = self.process_call_node(_node)
            elif isinstance(_node, ast.Constant):
                arg = _node.value
            else:
                arg = _node.id
            args.append(arg)
        value = CallOutput(
            call_name=call_name,
            args=args,
            kwargs=kwargs,
            lineno_start=node.lineno,
            lineno_end=node.end_lineno,
        )
        return value

    def process_default_value_from_ann_assign_node(
        self, node: Union[ast.Constant, None, _ast.Call]
    ) -> Union[None, str, Dict]:
        if node is None:
            return
        elif isinstance(node, ast.Constant):
            value = node.value
        elif isinstance(node, _ast.Call):
            value = self.process_call_node(node)
        else:
            value = node.func
            raise
        return value

    def process_ann_assing_node(
        self, node: ast.AnnAssign, _attrs: List
    ) -> List[VariableOutput]:
        name = node.target.id
        _type = self.process_annotation(node.annotation)

        value = self.process_default_value_from_ann_assign_node(node.value)

        _attr = VariableOutput(
            name=name,
            default=value,
            type_annotation=_type,
            lineno_start=node.lineno,
            lineno_end=node.end_lineno,
        )
        _attrs.append(_attr)
        return _attrs

    def process_class(self, node: ast.ClassDef) -> ClassOutput:
        _parents = []

        for base in node.bases:
            if isinstance(base, ast.Attribute):
                _parents.append(self.process_full_attr_node_name(base, None))
            else:
                _parents.append(base.id)

        _attrs = []

        for attr in node.body:
            # class scope of each class
            if isinstance(attr, ast.Assign):
                _attrs = self.process_assign_node(attr, _attrs)
            elif isinstance(attr, ast.AnnAssign):
                _attrs = self.process_ann_assing_node(attr, _attrs)

        _class = ClassOutput(
            name=node.name,
            parents=_parents,
            attrs=_attrs,
            lineno_start=node.lineno,
            lineno_end=node.end_lineno,
        )
        return _class

    def process_alias_node(self, node: _ast.alias) -> Dict:
        _alias = {"name": node.name, "alias": node.asname}
        return _alias

    def process_import_node(self, node: _ast.Import) -> List[ImportOutput]:
        node_lines = {"lineno_end": node.end_lineno, "lineno_start": node.lineno}
        imports = []
        for _import in node.names:
            _import = self.process_alias_node(_import)
            _import.update(node_lines)
            imports.append(ImportOutput(**_import))
        return imports

    def process_import_from(self, node: _ast.ImportFrom) -> FromImportOutput:
        node_lines = {"lineno_end": node.end_lineno, "lineno_start": node.lineno}
        imports = []
        for _import in node.names:
            _import = self.process_alias_node(_import)
            _import.update(node_lines)
            imports.append(_import)
        from_import = FromImportOutput(
            **node_lines, imports=imports, module=node.module
        )
        return from_import

    def process_expression_node(self, node: _ast.Expr):
        return self.process_call_node(node.value)

    def process_try_node(self, node: _ast.Try):
        try_nodes = []
        full_nodes_list = node.body + node.orelse + node.handlers + node.finalbody
        for _node in full_nodes_list:
            self.parse_node(_node, try_nodes)
        return try_nodes

    def process_if_node(self, node: _ast.If):
        if_nodes = []
        full_nodes_list = node.body + node.orelse
        for _node in full_nodes_list:
            self.parse_node(_node, if_nodes)
        return if_nodes

    def process_for_node(self, node: _ast.For):
        for_nodes = []
        full_nodes_list = [node.iter] + node.body + node.orelse
        for _node in full_nodes_list:
            self.parse_node(_node, for_nodes)
        return for_nodes

    def parse_return_node(self, node: _ast.Return):
        returns = []
        self.parse_node(node.value, returns)
        return returns

    def process_func_def_node(self, node: _ast.FunctionDef) -> FunctionOutput:
        decorators = []
        body = []
        returns = []
        for _node in node.body:
            print(type(_node))
            if isinstance(_node, _ast.Return):
                returns = self.parse_return_node(_node)
            else:
                self.parse_node(_node, body)
                print(body)

        for decorator in node.decorator_list:
            if isinstance(decorator, _ast.Call):
                decorators.append(self.process_call_node(decorator))
            elif isinstance(decorator, _ast.Name):
                decorators.append(NameOutput(name=decorator.id))
        return FunctionOutput(
            name=node.name,
            body=body,
            decorators=decorators,
            returns=returns,
            lineno_end=node.end_lineno,
            lineno_start=node.lineno,
        )

    """def process_tuple(self, node: _ast.Tuple):
        tuple_items = []
        for _node in node.elts:
            print(type(_node))
            self.parse_node(_node, tuple_items)
        print(tuple_items)
        raise
    """

    def parse_node(self, node: Any, output: OUTPUT_TYPE) -> OUTPUT_TYPE:
        # global scope of module
        if isinstance(node, _ast.Import):
            output.extend(self.process_import_node(node))
        elif isinstance(node, _ast.ImportFrom):
            output.append(self.process_import_from(node))
        elif isinstance(node, _ast.Expr):
            output.append(self.process_expression_node(node))
        elif isinstance(node, _ast.Try):
            output.extend(self.process_try_node(node))
        # elif isinstance(node, _ast.Tuple):
        # output.extend(self.process_tuple(node))
        elif isinstance(node, _ast.If):
            output.extend(self.process_if_node(node))
        elif isinstance(node, _ast.FunctionDef):
            output.extend(self.process_func_def_node(node))
        elif isinstance(node, _ast.For):
            output.extend(self.process_for_node(node))
        elif isinstance(node, _ast.Assign):
            output.extend(self.process_assign_node(node, []))
        elif isinstance(node, ast.ClassDef):
            output.append(self.process_class(node))

    def group_output_by_type(self, output: OUTPUT_TYPE):
        imports = []
        classes = []
        functions = []
        calls = []
        variables = []
        for node_out in output:
            node_type = node_out.node_type
            if node_type in [NodesTypes.IMPORT.value, NodesTypes.IMPORT_FROM.value]:
                imports.append(node_out)
            elif node_type == NodesTypes.CLASS.value:
                classes.append(node_type)
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

    def parse(self) -> Union[OUTPUT_TYPE, GroupNodesByType]:
        self.ast_tree = ast.parse(self.input_code)
        tree = self.ast_tree
        output = []
        for node in tree.body:
            self.parse_node(node, output)
        if self.group_by_type:
            output = self.group_output_by_type()
        return output
