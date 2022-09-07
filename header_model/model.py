
ACCESS_SPECIFIER_PUBLIC = "PUBLIC"
ACCESS_SPECIFIER_PROTECTED = "PROTECTED"
ACCESS_SPECIFIER_PRIVATE = "PRIVATE"


class CppOnlyElement:
    def __init__(self, source_element_text):
        self.source_text = source_element_text

    def __repr__(self):
        return self.source_text


class HeaderFileMethodModel:
    def __init__(self, return_type, name, access_specifier, is_const, is_static, has_override, argument_list=""):
        self.return_type = return_type
        self.name = name
        self.access_specifier = access_specifier
        self.is_const = is_const
        self.is_static = is_static
        self.has_override = has_override
        self.argument_list = "\n\t\t" + argument_list if argument_list else ""


class HeaderFileVariableModel:
    def __init__(self, access, static, const, type_name, variable_name, default_value_assignment):
        self.access = access
        self.static = static
        self.const = const
        self.type_name = type_name
        self.variable_name = variable_name
        self.default_value_assignment = default_value_assignment


class HeaderFileClassModel:
    def __init__(self, name, base_class):
        self.name = name
        self.methods = []
        self.member_variables = []
        self.base_class = base_class
        self.forward_declarations = []
        self.friend_decls = []

    def get_name(self):
        return self.name

    def add_method(self, method: HeaderFileMethodModel):
        self.methods.append(method)

    def get_methods(self):
        return self.methods

    def add_member_variable(self, variable: HeaderFileVariableModel):
        return self.member_variables.append(variable)

    def get_member_variables(self):
        return self.member_variables

    def get_base_class(self):
        return self.base_class

    def add_forward_declaration(self, type_name):
        if type_name not in self.forward_declarations:
            self.forward_declarations.append(type_name)

    def get_forward_declarations(self):
        return self.forward_declarations

    def has_init_method(self):
        for method in self.methods:
            if method.name == "init":
                return True
        return False

    def add_friend_decl(self, friend_decl):
        return self.friend_decls.append(friend_decl)

    def get_friend_decls(self):
        return self.friend_decls


class HeaderFileModel:
    def __init__(self):
        self.statements = []
        self.class_ = None
        self.includes = []
        self.typedefs = []
        self.forward_decls = []
        self.using_decls = []

    def add_statement(self, statement):
        self.statements.append(statement)

    def add_include(self, include):
        self.includes.append(include)

    def add_class(self, class_: HeaderFileClassModel):
        assert not self.class_, "Multiple class definitions not allowed"
        self.class_ = class_

    def get_class(self) -> HeaderFileClassModel:
        assert self.class_, "No class found in model"
        return self.class_

    def get_includes(self):
        return self.includes

    def add_typedefs(self, typedef):
        self.typedefs.append(typedef)

    def get_typedefs(self):
        return self.typedefs

    def add_forward_declaration(self, decl):
        self.forward_decls.append(decl)

    def get_forward_declaration(self):
        return self.forward_decls

    def add_using_declaration(self, using):
        self.using_decls.append(using)

    def get_using_declarations(self):
        return self.using_decls
