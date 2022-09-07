import os
import tempfile

from jinja2 import Environment, FileSystemLoader

from header_model.model import ACCESS_SPECIFIER_PROTECTED, ACCESS_SPECIFIER_PUBLIC, ACCESS_SPECIFIER_PRIVATE


class CppGenerationHelper:
    def __init__(self, model):
        self.model = model
        self.TYPE_INCLUDE_MAP = {
            "flags": '#include "flags/flags.h"',
        }

    def name(self):
        return self.model.get_class().get_name()

    def gen_class_declaration(self):
        decl = f"class {self.name()}"
        base_class = self.model.get_class().get_base_class()
        if base_class:
            decl += f" : public {base_class}"
        return decl

    def gen_system_includes_from_header(self):
        includes = [inc for inc in self.model.get_includes() if "<" in inc]
        if "#include <string>" not in includes:
            includes.insert(0, "#include <string>")
        return includes

    def _map_forward_declarations_to_includes(self):
        tokens = self.model.get_class().get_forward_declarations()

        includes = self._map_types_to_includes(tokens)
        return includes

    def _map_return_types_to_includes(self):
        methods = self.model.get_class().get_methods()
        tokens = [method.return_type for method in methods]

        includes = self._map_types_to_includes(tokens)

        return includes

    def _map_types_to_includes(self, tokens):
        includes = []
        for token in tokens:
            if token in self.TYPE_INCLUDE_MAP:
                includes.append(self.TYPE_INCLUDE_MAP[token])
        return includes

    def _map_argument_type_to_includes(self):
        all_includes = []
        methods = self.model.get_class().get_methods()
        for method in methods:
            tokens = method.argument_list.split()

            includes = self._map_types_to_includes(tokens)
            all_includes.extend(includes)

        return all_includes

    def _gen_project_includes_from_header(self):
        includes = [inc for inc in self.model.get_includes() if '"' in inc]

        includes.extend(self._map_forward_declarations_to_includes())
        includes.extend(self._map_return_types_to_includes())
        includes.extend(self._map_argument_type_to_includes())
        base_class = self.model.get_class().get_base_class()
        if base_class:
            includes.append(f'#include "{base_class}.h"')
        return includes

    def gen_includes(self):
        includes = self._gen_project_includes_from_header()
        return includes

    def _gen_forward_declarations_from_argument_types(self):
        decls = self.model.get_class().get_forward_declarations()
        ret = []
        for declaration in decls:
            ret.append(f"class {declaration};")
        return ret

    @staticmethod
    def _remove_duplicates(forward_decls):
        return list(dict.fromkeys(forward_decls))

    def gen_forward_declarations(self):
        forward_decls = self._gen_forward_declarations_from_argument_types()
        forward_decls.extend(self.model.get_forward_declaration())
        forward_decls = self._remove_duplicates(forward_decls)
        return forward_decls

    def gen_typedefs(self):
        return "\n".join(self.model.get_typedefs())

    def gen_friend_declarations(self):
        friend_decls = self.model.get_class().get_friend_decls()
        return "\n".join(friend_decls)

    @staticmethod
    def _map_types(argument_list):
        ARGUMENT_TYPE_MAP = {"long": "long int"}
        for k, v in ARGUMENT_TYPE_MAP.items():
            argument_list = argument_list.replace(k, v)
        return argument_list

    def gen_get_class_name(self):
        override = "override" if self.model.get_class().get_base_class() else ""
        code = "virtual std::string className() const " + override + ' {return "' + self.name() + '";}'
        return code

    def gen_cpp_methods(self):
        klass = self.model.get_class()
        visibility = "PUBLIC"
        for method in klass.get_methods():
            const_txt = " const " if method.is_const else ""
            override_txt = ""
            if method.name == "init":
                if len(method.argument_list) > 0 and not method.has_override:
                    override_txt = ""
                elif klass.get_base_class():
                    override_txt = "override"
            elif method.has_override:  # if in source: force 'override'
                override_txt = "override"

            static_or_virtual_txt = "static " if method.is_static else "virtual"
            return_type = self._map_types(method.return_type)
            visibility_code = ""
            if method.access_specifier != visibility:
                visibility_code = method.access_specifier.lower() + ":\n"
                visibility = method.access_specifier
            method_code = f"{visibility_code}\t{static_or_virtual_txt} {return_type} {method.name}({self._map_types(method.argument_list)}){const_txt} {override_txt};\n"
            yield method_code

    def has_init_method(self):
        return self.model.get_class().has_init_method()

    def _gen_member_variables(self, access_specifier):
        variables = self.model.get_class().get_member_variables()
        variables = [var for var in variables if var.access == access_specifier]
        code = ""
        for var in variables:
            static = "static" if var.static else ""
            const = "const" if var.const else ""
            type_name = self._map_types(var.type_name)
            code += f'{static} {const} {type_name} {var.variable_name} {var.default_value_assignment};'
        return code

    def gen_public_member_variables(self):
        return self._gen_member_variables(ACCESS_SPECIFIER_PUBLIC)

    def gen_protected_member_variables(self):
        return self._gen_member_variables(ACCESS_SPECIFIER_PROTECTED)

    def gen_private_member_variables(self):
        return self._gen_member_variables(ACCESS_SPECIFIER_PRIVATE)

    def gen_using_declarations(self):
        using_decls = self.model.get_using_declarations()
        return "\n".join(using_decls)


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATES_FOLDER = os.path.join(DIR_PATH, "templates")
MODULE_DIR = os.path.join(tempfile.gettempdir(), os.path.split(DIR_PATH)[-1])
ENCODING = 'ascii'
env = Environment(
    line_statement_prefix='%',
    line_comment_prefix='##',
    loader=FileSystemLoader(TEMPLATES_FOLDER, encoding=ENCODING),
    autoescape=False,
    auto_reload=True,  # set to false for performance improvement in production
    keep_trailing_newline=True,
    trim_blocks=False,
    lstrip_blocks=False
)


def generate_h_file(model):
    cpp_model = CppGenerationHelper(model)
    return _generate_output_file("CppHeaderTemplate.jinja2", cpp_model)


def _generate_output_file(template_file, cpp_model):
    template = env.get_template(template_file)
    templated_out_f = template.render(cpp_model=cpp_model)
    return templated_out_f
