from py_module_parser import PyModulesParser


def parse_from_file(file_path: str, **kwargs) -> dict:
    """function to call parser parse code from file"""
    with open(file_path, "r") as file_to_parse:
        data = file_to_parse.read()
        parser = PyModulesParser(data, **kwargs)
        return parser.parse()
