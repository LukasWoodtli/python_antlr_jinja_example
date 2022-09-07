grammar HeaderFile;

headerFile
   : statements? EOF
   ;

statements
   : statement statements?
   ;

statement
   : cppOnlyCode
   | preprocessorDirective
   | preprocessorInclude
   | typedef
   | forwardDeclaration
   | classDefinition
   | typedefPointerArray
   | usingDeclaration
   | globalVarDefinition
   | namespaceDeclaration
   | outStreamOperatorOverload
   | enumDefinition
   ;

classBody
   : classBodyElement*
   ;

classBodyElement
    : accessSpecifier Colon
    | memberFunctionDefinition
    | memberVariableDefinition
    | friendClassDeclaration
    | usingDeclaration
    ;

typedef
    : Typedef typeName Identifier Semicolon
    ;

typedefPointerArray
   : TypedefPointerArray
   ;

forwardDeclaration
    : Class className Semicolon
    | Struct className Semicolon
    ;

stdFunctionDecl
   : Identifier OpenParen typeNames CloseParen
   ;

usingDeclaration
   : Using Identifier Equals typeName Semicolon
   | Using typeName Semicolon
   ;

variableName
   : Identifier
   ;

staticVariableQualifier
   : Static
   ;

constVariableQualifier
   : Const
   ;

variableDefinition
   : staticVariableQualifier? constVariableQualifier? typeName variableName Semicolon
   | staticVariableQualifier? constVariableQualifier? typeName variableName defaultValueAssignment Semicolon
   ;

defaultValueAssignment
    : Equals typeName
    | Equals typeName OpenParen CloseParen
    | Equals StringLiteral
    | Equals Number
    ;

globalVarDefinition
   : variableDefinition
   ;


friendClassDeclaration
   : Friend Class typeName Semicolon
   ;

baseClassName
    : Identifier
    ;

classHead
   : Class className Final?
   | Class className Colon Public baseClassName Final?
   ;

classDefinition
   : classHead OpenBrace classBody CloseBrace Semicolon?
   ;

className
   : Identifier
   ;

typeNames
   : typeName
   | typeNames Coma typeName
   ;

typeName
    : valueTypeName
    | pointerTypeName
    | referenceTypeName
    | typeName OpenAngleBrackets typeNames CloseAngleBrackets
    | typeName OpenAngleBrackets stdFunctionDecl CloseAngleBrackets
    ;

valueTypeName
   : Const? fullQualifiedTypeNameElements+
   ;

pointerTypeName
   : valueTypeName Asterix Const?
    ;

referenceTypeName
   : valueTypeName Ampersand
   ;

fullQualifiedTypeNameElements
    : Identifier
    | NamespaceDelimiter
    ;

returnType
    : typeName
    ;

functionName
    : Identifier
    ;

constMethodQualifier
    : Const
    ;

overrideMethodQualifier
    : Override
    ;

virtualMethodQualifier
   : Virtual
   ;

unsafeMethodQualifier
   : Unsafe
   ;

staticMethodQualifier
   : Static
   ;

noWrapperMethodQualifier
   : NoWrapper
   ;

memberFunctionDefinition
    : noWrapperMethodQualifier? unsafeMethodQualifier? virtualMethodQualifier? staticMethodQualifier? returnType functionName OpenParen functionArgumentList? CloseParen constMethodQualifier? overrideMethodQualifier? Semicolon
    ;


memberVariableDefinition
   : variableDefinition
   ;


publicAccessSpecifier
   : Public
   ;

protectedAccessSpecifier
   : Protected
   ;

privateAccessSpecifier
   : Private
   ;

accessSpecifier
    : publicAccessSpecifier
    | protectedAccessSpecifier
    | privateAccessSpecifier
    ;

functionArgumentList
    : functionArgument
    | functionArgumentList Coma functionArgument
    ;

functionArgument
    : valueFunctionArgument
    | pointerFunctionArgument
    | referenceFunctionArgument
    | referencePointerFunctionArgument
    ;


valueFunctionArgument
    : Const? typeName argumentName defaultValueAssignment?
    ;

pointerFunctionArgument
    : Const? typeName Asterix Const? argumentName defaultValueAssignment?
    ;

referenceFunctionArgument
    : Const? typeName Ampersand argumentName defaultValueAssignment?
    ;

referencePointerFunctionArgument
    : Const? typeName Asterix Ampersand argumentName defaultValueAssignment?
    ;

argumentName
    : Identifier
    ;

cppOnlyCode
    : IfdefCPlusPlusCode statements Endif
    ;

preprocessorInclude
   : PreprocessorInclude
   ;

preprocessorDirective
   : Ifdef
   | Ifndef
   | Endif
   | Define
   | PragmaOnce
   ;

namespaceDeclaration
   : Namespace Identifier OpenBrace statements CloseBrace
   ;

outStreamOperatorOverload
   : typeName Ampersand? Operator OpenAngleBrackets OpenAngleBrackets OpenParen functionArgumentList CloseParen Semicolon
   ;

enumValues
   : Identifier
   | Identifier Coma enumValues
   ;

enumDefinition
   : Enum Class? Identifier OpenBrace enumValues CloseBrace Semicolon
   ;

Class
   : 'class'
   ;

Struct
   : 'struct'
   ;

Enum
   : 'enum'
   ;

Final
   : 'final'
   ;

Public : 'public';
Protected : 'protected';
Private :'private';

Const
    : 'const'
    ;

Override
    : 'override'
    ;

Typedef
    : 'typedef'
    ;

Virtual
   : 'virtual'
   ;

Friend
   : 'friend'
   ;

Using
   : 'using'
   ;

Static
   : 'static'
   ;

Operator
   : 'operator'
   ;

Namespace
   : 'namespace'
   ;

Unsafe
   : 'Unsafe'
   ;

NoWrapper
   : 'NoWrapper'
   ;

TypedefPointerArray
   : 'typedef PointerArray'
   ;

OpenBrace
    : '{'
    ;

CloseBrace
    : '}'
    ;

OpenParen
    : '('
    ;

CloseParen
    : ')'
    ;

OpenAngleBrackets
   : '<'
   ;

CloseAngleBrackets
   : '>'
   ;

Semicolon
   : ';'
   ;

Coma
    : ','
    ;

Colon
    : ':'
    ;

Asterix
    : '*'
    ;

Ampersand
    : '&'
    ;

NamespaceDelimiter
    : '::'
    ;

Equals
    : '='
    ;

Number
   : [0-9]+ 'U'?
   ;

Identifier
   : [a-zA-Z][a-zA-Z0-9_]*;


fragment IncludePath
   : [a-zA-Z0-9/_.]+?
   ;

PreprocessorInclude
   : '#' [ \t]*? 'include' [ \t]+ '"' IncludePath '"'
   | '#' [ \t]*? 'include' [ \t]+ '<' IncludePath '>'
   ;


IfdefCPlusPlusCode
   : '#' 'ifdef CPlusPlusCode' [\r]?[\n]
   ;

Endif : '#' 'endif' [\r]?[\n];


Ifdef
   : '#' 'ifdef' (~ [\r\n]+)+? [\r]?[\n]
   ;

Ifndef
   : '#' 'ifndef' (~ [\r\n]+)+? [\r]?[\n]
   ;

Define
   : '#' 'define' (~ [\r\n]+)+? [\r]?[\n]
   ;


PragmaOnce : '#' [ \t]* 'pragma' [ \t]+ 'once' [\r]?[\n];

StringLiteral
   : '"' (~["])* '"'
   ;

BlockComment
   : '/*' .*? '*/' -> skip
   ;

LineComment
   : '//' ~[\r\n]* -> skip
   ;

WS : [ \t\r\n]+ -> skip ;
