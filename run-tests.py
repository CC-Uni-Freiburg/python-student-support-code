import os
from sys import platform
import interp_Lfun
import interp_Cfun
import type_check_Lfun
import type_check_Cfun
import generate_tests
import utils
from interp_x86.eval_x86 import interp_x86
from compiler import Compiler

# Generate Tests from compact test files
generate_tests.generate_all_tests()

# Generate runtime.o for linking with the compiled x86 programs
if not os.path.isfile("runtime.o"):
    # This might produce a warning which normally can be ignored
    if platform == "darwin":
        os.system("gcc -c -g -std=c99 -arch x86_64 runtime.c")
    else:
        os.system("gcc -c -g -std=c99 runtime.c")

# Execute tests

type_check_L = type_check_Lfun.TypeCheckLfun()
type_check_C = type_check_Cfun.TypeCheckCfun()
interp_L = interp_Lfun.InterpLfun()
interp_C = interp_Cfun.InterpCfun()
compiler = Compiler()

typecheck_dict = {
    "source": type_check_L.type_check,
    "shrink": type_check_L.type_check,
    "reveal_functions": type_check_L.type_check,
    "limit_functions": type_check_L.type_check,
    "expose_allocation": type_check_L.type_check,
    "remove_complex_operands": type_check_L.type_check,
    "explicate_control": type_check_C.type_check,
}
interp_dict = {
    "source": interp_L.interp,
    "shrink": interp_L.interp,
    "reveal_functions": interp_L.interp,
    "limit_functions": interp_L.interp,
    "expose_allocation": interp_L.interp,
    "remove_complex_operands": interp_L.interp,
    "explicate_control": interp_C.interp,
    "select_instructions": interp_x86,
    "assign_homes": interp_x86,
    "patch_instructions": interp_x86,
}

# Set this to False for single test checking
if True:
    # Set this to True if you want to check if testing is still progressing
    utils.verbose = False
    # Set this to True if you want to see the output of the compiler
    utils.tracing = False
    # Here you can set the tests that should be checked
    succ = True
    for lang in "var regalloc lif tuples fun".split():
        succ = succ and utils.run_tests(
            lang, compiler, lang, typecheck_dict, interp_dict
        )
    if succ:
        print("All tests passed!")
else:
    # In case you only want to test a single test file
    # you can enable the execution of this branch
    utils.tracing = False
    utils.run_one_test(
        os.getcwd() + "/tests/var/zero.py",
        "single",
        compiler,
        "single",
        typecheck_dict,
        interp_dict,
    )
