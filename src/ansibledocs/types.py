class Variable:
    def __init__(self, name, value=None, description="", required=False, vars_defaults='-'):
        self.name = name
        self.required = required
        self.vars_defaults = vars_defaults
        if value is None:
            self.value = '-'
            self.var_type = '-'
        else:
            self.value = value
            self.var_type = type(value).__name__
        self.description = description


class Role:
    def __init__(self, name, description, tasks=None, variables=None):
        if variables is None:
            variables = {}
        if tasks is None:
            tasks = []
        self.name = name
        self.description = description
        self.tasks = tasks
        self.variables = variables
