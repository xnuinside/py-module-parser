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
print("Result: \n")
print(parsed_output)
