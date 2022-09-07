import os

from approvaltests.approvals import verify

import templated_code_generation
from parse_header import parse_header_file


input_file = os.path.dirname(__file__)
input_file = os.path.join(input_file, "input_files", "TestInputFile.h")


def test_parse_file():
    model = parse_header_file(input_file)
    assert model.get_class().get_name() == "TestExampleClass"


def test_generate_files():
    model = parse_header_file(input_file)
    generated_code = templated_code_generation.generate_h_file(model)

    verify(generated_code)

