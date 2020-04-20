import yaml

from .types import Variable


class VarsParser:
    vars_to_remove = [
        # Special variables
        # https://docs.ansible.com/ansible/latest/reference_appendices/special_variables.html
        'ansible_check_mode', 'ansible_dependent_role_names', 'ansible_diff_mode', 'ansible_forks',
        'ansible_inventory_sources', 'ansible_limit', 'ansible_loop', 'ansible_loop_var', 'ansible_index_var',
        'ansible_parent_role_names', 'ansible_parent_role_paths', 'ansible_play_batch', 'ansible_play_hosts',
        'ansible_play_hosts_all', 'ansible_play_role_names', 'ansible_playbook_python', 'ansible_role_names',
        'ansible_run_tags', 'ansible_search_path', 'ansible_skip_tags', 'ansible_verbosity', 'ansible_version',
        'group_names', 'groups', 'hostvars', 'inventory_hostname', 'inventory_hostname_short', 'inventory_dir',
        'inventory_file', 'omit', 'play_hosts', 'ansible_play_name', 'playbook_dir', 'role_name', 'role_names',
        'role_path', 'ansible_facts', 'ansible_local', 'ansible_become_user', 'ansible_connection', 'ansible_host',
        'ansible_python_interpreter', 'ansible_user',
        # Other variables
        'item']

    def cleanup(self, vars_dict):
        dict_copy = vars_dict.copy()
        for key in list(dict_copy):
            if key in self.vars_to_remove:
                del dict_copy[key]

        return dict_copy

    def __associate_comments(self, yaml_str):
        comments_dict = {}
        comment = ""
        for line in yaml_str.splitlines():
            if line.startswith('#'):
                comment += line[1:].replace(' ', '&nbsp;') + '<br/>'
            elif line and not line[0].isspace():
                comments_dict[line.split(':')[0]] = comment
                comment = ""
            else:
                comment = ""

        return comments_dict

    def parse(self, file_path, vars_defaults, vars_dict):
        try:
            # Open variables file
            with open(file_path, "r") as stream:
                # Parse variables file with yaml parser
                try:
                  variables = yaml.safe_load(stream)
                except:
                  print(f"Error parsing '{file_path}'")
                  return vars_dict

                # Validation for 'vaulted', empty vars files
                if type(variables) is str:
                  print("File is 'vaulted'. Skipping")
                  return vars_dict
                elif variables is None:
                  print("File is empty. Skipping")
                  return vars_dict

                stream.seek(0)
                comments = self.__associate_comments(stream.read())

                # Run on each variables key
                for key, value in variables.items():
                    vars_dict[key] = Variable(name=key, value=value, vars_defaults=vars_defaults, description=comments[key])
        except yaml.YAMLError as exc:
            raise exc

        return vars_dict
