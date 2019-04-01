import os
import jinja2
import sys
import importlib 
import inspect

# Dynamic import for module of interest
arg = sys.argv[1]
path_to_module, module_name = os.path.split(arg)
module_name = os.path.splitext(module_name)[0]
sys.path.append(path_to_module)
module = importlib.import_module(module_name)
clsmembers = [classname for classname, obj in inspect.getmembers(module, inspect.isclass)]

# Create jinja template
env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
template = env.get_template('test_template.py').render(module_name = module_name, class_name = clsmembers[0])

# Create tests directory and autogenerate the test class
test_dir = os.path.join(path_to_module, 'tests')
if not os.path.exists(test_dir):
    os.makedirs(test_dir)

test_filename = os.path.join(test_dir, 'test_{}_.py'.format(module_name))
with open(test_filename, 'w') as test_file:
    print(template, file=test_file)
