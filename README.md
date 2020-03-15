### Ansible docs generator

Helper tool used to generate ansible documentation.

### Features:
* Parse role folder and generate readme file
* Vars/Defaults variables parsing (Comments before variable will be added to description)
* Tasks parsing

### TODO:
* add ansible jinja2 custom filters https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#playbooks-filters
* think about deleting all ansible_* vars from list since we have a lot of them in the ansible_facts
* remove registered vars from list
* expand block tasks
* can we parse tasks type?
* parse role description from meta
* fix fail on empty vars file
* add ansible-vault support

Thanks for inspiration to https://github.com/RcRonco/role2md