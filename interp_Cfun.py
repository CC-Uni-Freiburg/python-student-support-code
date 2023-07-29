import ast
from interp_Ctup import InterpCtup
import utils
from interp_Lfun import Function


class InterpCfun(InterpCtup):
    def apply_fun(self, fun, args, e):
        match fun:
            case Function(name, xs, blocks, env):
                old_blocks = self.blocks
                self.blocks = blocks
                # trace('apply_fun ' + name)
                # trace(blocks.keys())
                new_env = env.copy()
                for (x, arg) in zip(xs, args):
                    new_env[x] = arg

                next_label = name + "start"
                ret = None
                while True:
                    r = self.interp_stmts(blocks[utils.label_name(next_label)], new_env)
                    match r:
                        case utils.Goto(label):
                            next_label = label
                        case utils.TailCallHelper(func, args, env):
                            new_env = env.copy()
                            for (x, arg) in zip(xs, args):
                                new_env[x] = arg
                            next_label = getattr(func, "name") + "start"
                        case ast.Return(retval):
                            ret = retval
                            break
                        case _:
                            raise Exception("apply_fun: unexpected return " + repr(r))
                self.blocks = old_blocks
                return ret
            case _:
                raise Exception("apply_fun: unexpected: " + repr(fun))

    def interp_exp(self, e, env):
        match e:
            case ast.Call(ast.Name("input_int"), []):
                return super().interp_exp(e, env)
            case ast.Call(ast.Name("len"), [tup]):
                return super().interp_exp(e, env)
            case ast.Call(func, args):
                f = self.interp_exp(func, env)
                vs = [self.interp_exp(arg, env) for arg in args]
                return self.apply_fun(f, vs, e)
            case utils.FunRef(id, arity):
                return env[id]
            case _:
                return super().interp_exp(e, env)

    def interp_stmts(self, ss, env):
        if len(ss) == 0:
            raise Exception("interp_stmts function ended without return")
        match ss[0]:
            case utils.TailCall(func, args):
                # return self.interp_exp(ast.Call(func, args), env)
                f = self.interp_exp(func, env)
                vs = [self.interp_exp(arg, env) for arg in args]
                return utils.TailCallHelper(f, vs, env)  # type: ignore
            case _:
                return super().interp_stmts(ss, env)

    def interp(self, p):
        match p:
            case utils.CProgramDefs(defs):
                env = {}
                for d in defs:
                    match d:
                        case ast.FunctionDef(
                            name, params, blocks, dl, returns, comment
                        ):
                            env[name] = Function(
                                name, [x for (x, t) in params], blocks, env  # type: ignore
                            )
                self.blocks = {}
                self.apply_fun(env["main"], [], None)
            case _:
                raise Exception("interp: unexpected " + repr(p))
