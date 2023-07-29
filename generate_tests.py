import os
import sys
import re

def generate_tests(path, filename):
    """
    Converts a multi-test file into a set of test cases (in the subdirectory
    specified by path).

    A multi-test file consists of n times the format:

    #begin#
    <filename>
    #py#
    <.py content>
    #in#
    <.in content>
    #golden#
    <.golden content>
    #end#

    E.g. applying generate_tests to a file with the content:

    #begin#
    print_1
    #py#
    print(1)
    #in#
    #golden#
    1
    #end#

    #begin#
    print_2
    #py#
    print(2)
    #in#
    #golden#
    2
    #end#

    creates print_1.py, print_1.in and print_1.golden, as well as
    print_2.py, print_2.in and print_2.golden with the corresponding content.
    """
    try:
        raw = []
        with open(os.path.join(path, filename), "r") as file:
            raw = file.read()
        for test in re.findall("#begin#\n.*?#end#", raw, re.DOTALL):
            name = test.split("\n")[1]
            py_content = re.findall("#py#\n.*?#in#", test, re.DOTALL)[0][len("#py#\n"):-len("#in#")]
            in_content = re.findall("#in#\n.*?#golden#", test, re.DOTALL)[0][len("#in#\n"):-len("#golden#")]
            golden_content = re.findall("#golden#\n.*?#end#", test, re.DOTALL)[0][len("#golden#\n"):-len("#end#")]
            with open(os.path.join(path, name + ".py"), "w") as file:
                file.write(py_content)
            with open(os.path.join(path, name + ".in"), "w") as file:
                file.write(in_content)
            with open(os.path.join(path, name + ".golden"), "w") as file:
                file.write(golden_content)
    except Exception as e:
        print(f"Something went wrong while generating tests from {os.path.join(path, filename)}\n")
        print("generate_tests help:")
        print(generate_tests.__doc__)
        raise e

def generate_all_tests():
    """
    Applies generate_tests to all ".tests" files in the "tests" directory and its
    subdirectories e.g. tests/var/example.tests.
    """
    for subdir, dirs, files in os.walk("tests"):
        for file in files:
            if os.path.splitext(file)[1] == ".tests":
                generate_tests(subdir, file)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("generate_all_teststs help:")
        print(generate_all_tests.__doc__)
        exit(0)
    if not os.path.isdir("tests"):
        print("tests/ directory is missing\n")
        print("generate_all_teststs help:")
        print(generate_all_tests.__doc__)
        exit(0)
    generate_all_tests()
