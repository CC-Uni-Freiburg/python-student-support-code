import ast
import utils
from type_check_Ctup import TypeCheckCtup
import copy


class TypeCheckCfun(TypeCheckCtup):
    def check_type_equal(self, t1, t2, e):
        if t1 == utils.Bottom() or t2 == utils.Bottom():
            return
        match t1:
            case utils.FunctionType(ps1, rt1):
                match t2:
                    case utils.FunctionType(ps2, rt2):
                        self.check_type_equal(rt1, rt2, e)
                        for (p1, p2) in zip(ps1, ps2):
                            self.check_type_equal(p1, p2, e)
                    case _:
                        raise Exception(
                            "error: "
                            + repr(t1)
                            + " != "
                            + repr(t2)
                            + " in "
                            + repr(e)
                        )
            case _:
                super().check_type_equal(t1, t2, e)

    def type_check_exp(self, e, env):
        match e:
            case ast.Constant(None):
                return utils.VoidType()
            case utils.FunRef(id, arity):
                return env[id]
            case ast.Call(ast.Name("input_int"), []):
                return super().type_check_exp(e, env)
            case ast.Call(ast.Name("len"), [tup]):
                return super().type_check_exp(e, env)
            case ast.Call(func, args):
                func_t = self.type_check_exp(func, env)
                args_t = [self.type_check_exp(arg, env) for arg in args]
                match func_t:
                    case utils.FunctionType(params_t, return_t):
                        for (arg_t, param_t) in zip(args_t, params_t):
                            self.check_type_equal(param_t, arg_t, e)
                        return return_t
                    case utils.Bottom():
                        return utils.Bottom()
                    case _:
                        raise Exception(
                            "type_check_exp: in call, unexpected "
                            + repr(func_t)
                        )
            case _:
                return super().type_check_exp(e, env)

    def type_check_def(self, d, env):
        match d:
            case ast.FunctionDef(name, params, blocks, dl, returns, comment):
                new_env = {x: t for (x, t) in env.items()}
                for (x, t) in params:  # type: ignore
                    new_env[x] = t
                while True:
                    old_env = copy.deepcopy(new_env)
                    for (l, ss) in blocks.items():  # type: ignore
                        self.type_check_stmts(ss, new_env)
                    # trace('type_check_Cfun iterating ' + repr(new_env))
                    if new_env == old_env:
                        break
                # todo check return type
                d.var_types = new_env  # type: ignore
                # trace('type_check_Cfun var_types for ' + name)
                # trace(d.var_types)
            case _:
                raise Exception(
                    "type_check_def: unexpected "
                    + repr(d)
                )

    def type_check_stmt(self, s, env):
        match s:
            case ast.Return(value):
                self.type_check_exp(value, env)
            case utils.TailCall(func, args):
                self.type_check_exp(ast.Call(func, args), env)
            case _:
                super().type_check_stmt(s, env)

    def type_check(self, p):
        match p:
            case utils.CProgramDefs(defs):
                env = {}
                for d in defs:
                    match d:
                        case ast.FunctionDef(name, params, bod, dl, returns, comment):
                            params_t = [t for (x, t) in params]  # type: ignore
                            env[name] = utils.FunctionType(params_t, returns)  # type: ignore
                for d in defs:
                    self.type_check_def(d, env)
            case _:
                raise Exception("type_check: unexpected " + repr(p))
