from py_module_parser import PyModulesParser

source_code = """from django.db import models


class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)


@decor(params=1)
@decor2
def some_function(arg: str, arg2=None):
    arg = 'any'
    return arg, '1'

"""
parsed_output = PyModulesParser(source_code).parse()
print("Result \n")
print(parsed_output)

# you can also use parsed_output.group_by_type().json()
# to get json output grouped by type
parsed_output_group = parsed_output.group_by_type()
print("Result group_by_type: \n")
print(parsed_output_group)

# you can also use parsed_output.group_by_type().json()
# to get json output grouped by type
parsed_output_group_dict = parsed_output.group_by_type().model_dump()
print("Result as python dict: \n")
print(parsed_output_group_dict)


parsed_output_json = parsed_output.json()
print("Result in json: \n")
print(parsed_output_json)
