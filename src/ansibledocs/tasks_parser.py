import yaml

from .types import Variable
from jinja2 import Environment, meta


def get_tasks_file_vars(file_path):
    # Parse yaml tasks
    with open(file_path, "r") as stream:
        tasks = yaml.safe_load(stream)
        for task in tasks:
            # Surround when statement with {{ }} so jinja2 can parse it
            if 'when' in task:
                task['when'] = f"{{{{ {task['when']} }}}}"

        # Parse the content of the template
        parsed_content = Environment().parse(tasks)

        # Get undeclared variable that in use
        task_vars = meta.find_undeclared_variables(parsed_content)
        vars_dict = {}
        for var in task_vars:
            vars_dict[var] = Variable(var, required="Yes")

        return vars_dict


def parse_tasks(file_path, tasks_list, vars_dict):
    try:
        # Get tasks file variables
        vars_dict = get_tasks_file_vars(file_path)
        # Open tasks file
        with open(file_path, "r") as stream:
            tasks = yaml.safe_load(stream)

            # Run on tasks entry
            for task in tasks:
                if 'name' in task:
                    tasks_list.append(task['name'])
                else:
                    tasks_list.append(f"Name does't specified for task: {task}")
    except yaml.YAMLError as exc:
        print(exc)

    return tasks_list, vars_dict
