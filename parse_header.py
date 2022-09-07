from antlr4.error.ErrorListener import ErrorListener

from header_model.model import HeaderFileModel, ACCESS_SPECIFIER_PUBLIC, HeaderFileClassModel, HeaderFileMethodModel, \
    CppOnlyElement, HeaderFileVariableModel, ACCESS_SPECIFIER_PRIVATE, ACCESS_SPECIFIER_PROTECTED
from antlr4.BufferedTokenStream import BufferedTokenStream

from parsing.HeaderFileParser import *
from parsing.HeaderFileLexer import HeaderFileLexer
from parsing.HeaderFileListener import HeaderFileListener


class HeaderFileErrorListener(ErrorListener):

    def __init__(self) -> None:
        super(HeaderFileErrorListener, self).__init__()

    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        super().syntaxError(recognizer, offending_symbol, line, column, msg, e)
        raise Exception(f"Error at line {line}:{column} {msg}")


class HeaderFileModelCreator(HeaderFileListener):
    def __init__(self, parser):
        self.parser = parser
        self.header_file_model = HeaderFileModel()
        self.current_class = None
        self.current_access_modifier = ACCESS_SPECIFIER_PUBLIC

    def _get_source_location(self, ctx):
        return f"{self.header_file_model.name}: {ctx.start.line}, {ctx.start.column}"

# This helps debugging
#     def __getattribute__(self, name):
#         attr = object.__getattribute__(self, name)
#         if hasattr(attr, '__call__'):
#             def newfunc(*args, **kwargs):
#                 print('before calling %s with args %s and %s' % (attr.__name__, str(args), str(kwargs)))
#                 result = attr(*args, **kwargs)
#                 #print('done calling %s' % attr.__name__)
#                 return result
#
#             return newfunc
#         else:
#             return attr

    def get_model(self) -> HeaderFileModel:
        return self.header_file_model

    @staticmethod
    def _get_original_source_code(element):
        stream = element.start.getInputStream()
        arg_list_start = element.start.start
        arg_list_end = element.stop.stop
        element_source_code = stream.strdata[arg_list_start:arg_list_end + 1]
        return element_source_code

    def enterPreprocessorDirective(self, context: HeaderFileParser.PreprocessorDirectiveContext):
        self.header_file_model.add_statement(CppOnlyElement(context.getText().strip("\n")))

    def enterPreprocessorInclude(self, context: HeaderFileParser.PreprocessorIncludeContext):
        self.header_file_model.add_include(context.getText().strip("\n"))

    def enterClassDefinition(self, context: HeaderFileParser.ClassDefinitionContext):
        assert self.current_class == None, f"No nested classes allowed: {self._get_source_location(context)}"
        base_class = context.classHead().baseClassName()
        base_class_name = base_class.getText() if base_class else ""
        self.current_class = HeaderFileClassModel(context.classHead().className().getText(),
                                               base_class_name)

    def exitClassDefinition(self, context: HeaderFileParser.ClassDefinitionContext):
        self.header_file_model.add_class(self.current_class)

    def exitPublicAccessSpecifier(self, context):
        self.current_access_modifier = ACCESS_SPECIFIER_PUBLIC

    def exitProtectedAccessSpecifier(self, context):
        self.current_access_modifier = ACCESS_SPECIFIER_PROTECTED

    def exitPrivateAccessSpecifier(self, context):
        self.current_access_modifier = ACCESS_SPECIFIER_PRIVATE

    def exitMemberFunctionDefinition(self, context: HeaderFileParser.MemberFunctionDefinitionContext):
        assert self.current_class, f"No class defined: {self._get_source_location(context)}"

        is_const = True if context.constMethodQualifier() else False
        is_static = True if context.staticMethodQualifier() else False
        has_override = True if context.overrideMethodQualifier() else False
        return_type = self._get_original_source_code(context.returnType())
        function_name = context.functionName().getText()
        arg_list = context.functionArgumentList()

        arg_list_text = self._get_original_source_code(arg_list) if arg_list else ""

        method = HeaderFileMethodModel(return_type,
                                    function_name,
                                    self.current_access_modifier,
                                    is_const,
                                    is_static,
                                    has_override,
                                    arg_list_text)
        self.current_class.add_method(method)

    def exitMemberVariableDefinition(self, context: HeaderFileParser.MemberVariableDefinitionContext):
        assert self.current_class, f"No class defined: {self._get_source_location(context)}"

        access_modifier = self.current_access_modifier
        variable_context = context.variableDefinition()
        static = True if variable_context.staticVariableQualifier() else False
        const = True if variable_context.constVariableQualifier() else False
        type_name = variable_context.typeName().getText()
        variable_name = variable_context.variableName().getText()
        default_value = variable_context.defaultValueAssignment()
        default_value_assignment = self._get_original_source_code(default_value) if default_value else ""

        member_variable = HeaderFileVariableModel(access_modifier, static, const, type_name, variable_name, default_value_assignment)
        self.current_class.add_member_variable(member_variable)

    def exitTypedef(self, context: HeaderFileParser.TypedefContext):
        typedef = self._get_original_source_code(context)
        self.header_file_model.add_typedefs(typedef)

    def exitUsingDeclaration(self, context:HeaderFileParser.UsingDeclarationContext):
        using = self._get_original_source_code(context)
        self.header_file_model.add_using_declaration(using)

    def exitForwardDeclaration(self, ctx: HeaderFileParser.ForwardDeclarationContext):
        decl = self._get_original_source_code(ctx)
        self.header_file_model.add_forward_declaration(decl)

    def _add_type_for_forward_declaration(self, context: HeaderFileParser.ValueTypeNameContext):
        if self.current_class:
            type_name = ""
            for element in context.fullQualifiedTypeNameElements():
                type_name += self._get_original_source_code(element)

            self.current_class.add_forward_declaration(type_name)

    def exitFriendClassDeclaration(self, ctx:HeaderFileParser.FriendClassDeclarationContext):
        self.current_class.add_friend_decl(self._get_original_source_code(ctx))

    def exitPointerTypeName(self, context: HeaderFileParser.PointerTypeNameContext):
        self._add_type_for_forward_declaration(context.valueTypeName())

    def exitReferenceTypeName(self, context: HeaderFileParser.PointerTypeNameContext):
        self._add_type_for_forward_declaration(context.valueTypeName())


def parse_header_file(filename):
    print(f"Parsing: {filename}")
    input_stream = FileStream(filename, encoding='iso-8859-1')
    lexer = HeaderFileLexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(HeaderFileErrorListener())
    stream = BufferedTokenStream.BufferedTokenStream(lexer)
    parser = HeaderFileParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(HeaderFileErrorListener())

    try:
        tree = parser.headerFile()
    except Exception as err:
        error_msg = f"Error occured while parsing: {filename}\n\t"
        raise Exception(error_msg + str(err))

    listener = HeaderFileModelCreator(parser)
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    return listener.get_model()
