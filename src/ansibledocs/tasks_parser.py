import yaml

from .types import Variable
from jinja2 import Environment, meta
from ansible.plugins.filter.core import FilterModule
from ansible.parsing.mod_args import ModuleArgsParser
from ansible.utils.sentinel import Sentinel

# https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html
custom_filters = FilterModule().filters()


def get_tasks_file_vars(file_path):
    # Parse yaml tasks
    with open(file_path, "r") as stream:
        tasks = yaml.safe_load(stream)
        for task in tasks:
            # Surround when statement with {{ }} so jinja2 can parse it
            if 'when' in task:
                task['when'] = f"{{{{ {task['when']} }}}}"

        environment = Environment()
        # Add dummy ansible jinja2 custom filters
        for filter in custom_filters:
            environment.filters[filter] = lambda: None
        # Parse the content of the template
        parsed_content = environment.parse(tasks)

        # Get undeclared variable that in use
        task_vars = meta.find_undeclared_variables(parsed_content)
        vars_dict = {}
        for var in task_vars:
            vars_dict[var] = Variable(var, required="Yes")

        return vars_dict

def parse_task(task):
  if 'block' in task:
    print("BLOCK")
    return 'block', '', ''
  else:
    (action, args, delegate_to) = ModuleArgsParser(task).parse(skip_action_validation=True)
    if action in ('include', 'import_tasks', 'include_tasks'):
      print("include task")
    elif action in ('include_role', 'import_role'):
      print("include role")

    return action, args, ( delegate_to if delegate_to is not Sentinel else None)


def parse_tasks(file_path, tasks_list, vars_dict):
    try:
        # Get tasks file variables
        vars_dict = get_tasks_file_vars(file_path)
        # Open tasks file
        with open(file_path, "r") as stream:
            tasks = yaml.safe_load(stream)

            # Run on tasks entry
            for task in tasks:
                print(parse_task(task))           
                if 'name' in task:
                    tasks_list.append(task['name'])
                else:
                    tasks_list.append(f"Name does't specified for task: {task}")
    except yaml.YAMLError as exc:
        print(exc)

    return tasks_list, vars_dict
