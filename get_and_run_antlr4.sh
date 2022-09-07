#!/bin/bash

set -e

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

cd $script_dir

jar_name=antlr-4.7.1-complete.jar

if [ ! -f $jar_name ]; then
    curl -O https://www.antlr.org/download/$jar_name
fi

export CLASSPATH=".:$script_dir/$jar_name:$CLASSPATH"
antlr4="java -jar $script_dir/$jar_name"


cd parsing

$antlr4 -Dlanguage=Python3 HeaderFile.g4 -o .
