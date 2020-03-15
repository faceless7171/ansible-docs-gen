import argparse
import sys
import os

from jinja2 import Environment, FileSystemLoader
from src.ansibledocs.variables_parser import VarsParser
from src.ansibledocs.tasks_parser import parse_tasks
from src.ansibledocs.types import Role


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Generate documentation for ansible role")
    parser.add_argument('-s', '--src', required=True, type=str, help="The path to the ansbile role")
    parser.add_argument('-d', '--dest', required=True, type=str, help="The path to the output Markdown document")
    parser.add_argument('-f', '--force', action='store_true', help="If file is already exist force rewrite")
    args = parser.parse_args(argv)

    return args.src, args.dest, args.force

def main(argv):
    src, dest, force = parse_args(argv)

    role = Role(os.path.basename(src), 'No description')
    types = ["defaults", "vars"]

    if os.path.exists(dest) and not force:
        force_str = input("The output destination already exists do you want to rewrite?(y/n)")
        if force_str != 'y':
            exit(0)

    if not os.path.exists(src):
        raise Exception(f"{src} does not exists.")

    if os.path.exists(os.path.join(src, "tasks")):
        for path, _, files in os.walk(os.path.join(src, "tasks")):
            for file in files:
                role.tasks, role.variables = parse_tasks((os.path.join(path, file)), role.tasks, role.variables)
                print(f"Tasks: {os.path.join(path, file)}")

    vars_parser = VarsParser()
    if os.path.exists(os.path.join(src, "defaults")):
        for path, _, files in os.walk(os.path.join(src, "defaults")):
            for file in files:
                role.variables = vars_parser.parse((os.path.join(path, file)), types[0], role.variables)
                print(f"Defaults: {os.path.join(path, file)}")

    if os.path.exists(os.path.join(src, "vars")):
        for path, _, files in os.walk(os.path.join(src, "vars")):
            for file in files:
                role.variables = vars_parser.parse((os.path.join(path, file)), types[1], role.variables)
                print(f"Vars: {os.path.join(path, file)}")

    role.variables = vars_parser.cleanup(role.variables)
    with open(dest, "w") as fd:
        # Generate the markdown table from the collected variables
        fd.write(build_rdme(role))


def build_rdme(role):
    env = Environment(loader=FileSystemLoader(searchpath="src/templates"))
    template = env.get_template('role.jinja2')
    return template.render(role=role)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

