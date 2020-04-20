### Ansible docs generator

Helper tool used to generate ansible documentation.

### Features:
* Parse role folder and generate readme file
* Vars/Defaults variables parsing (Comments before variable will be added to description)
* Tasks parsing

### How to run:

```
pip3 install -r requirements.txt
python3 main.py -h
```  

### TODO:
* think about deleting all ansible_* vars from list since we have a lot of them in the ansible_facts
* remove registered vars from list
* expand block tasks
* can we parse tasks type?
* parse role description from meta
* iterate only over *.yml *.yaml files

Thanks for inspiration to https://github.com/RcRonco/role2md