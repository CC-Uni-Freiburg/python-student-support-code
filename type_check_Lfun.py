import ast
from types import NoneType
from type_check_Ltup import TypeCheckLtup
import utils
from types import NoneType


class TypeCheckLfun(TypeCheckLtup):
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

    def parse_type_annot(self, annot):
        match annot:
            case ast.Name(id):
                if id == "int":
                    return utils.IntType()
                elif id == "bool":
                    return utils.BoolType()
                else:
                    raise Exception(
                        "parse_type_annot: unexpected "
                        + repr(annot)
                    )
            case utils.TupleType(ts):
                return utils.TupleType([self.parse_type_annot(t) for t in ts])  # type: ignore
            case utils.ListType(t):
                return utils.ListType(self.parse_type_annot(t))
            case utils.FunctionType(ps, rt):
                return utils.FunctionType(
                    [self.parse_type_annot(t) for t in ps], self.parse_type_annot(rt)
                )
            case ast.Subscript(ast.Name("Callable"), ast.Tuple([ps, rt])):
                return utils.FunctionType(
                    [self.parse_type_annot(t) for t in ps.elts],  # type: ignore
                    self.parse_type_annot(rt),
                )
            case ast.Subscript(ast.Name("tuple"), ast.Tuple(ts)):
                return utils.TupleType([self.parse_type_annot(t) for t in ts])
            case ast.Subscript(ast.Name('tuple'), t):
                return utils.TupleType([self.parse_type_annot(t)])
            case ast.Subscript(ast.Name("list"), t):
                ty = self.parse_type_annot(t)
                return utils.ListType(ty)
            case utils.IntType() | utils.BoolType() | utils.VoidType():
                return annot
            case t if t == int:
                return utils.IntType()
            case t if t == bool:
                return utils.BoolType()
            case t if t == NoneType:
                return utils.VoidType()
            case ast.Constant(None) | None:
                return utils.VoidType()
            case _:
                raise Exception(
                    "parse_type_annot: unexpected "
                    + repr(annot)
                )

    def type_check_exp(self, e, env):
        match e:
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
                    case _:
                        raise Exception(
                            "type_check_exp: in call, unexpected "
                            + repr(func_t)
                        )
            case _:
                return super().type_check_exp(e, env)

    def type_check_stmts(self, ss, env):
        if len(ss) == 0:
          return
        match ss[0]:
          case ast.FunctionDef(name, params, body, dl, returns, comment):
            new_env = {x: t for (x,t) in env.items()}
            if isinstance(params, ast.arguments):
                new_params = [(p.arg, self.parse_type_annot(p.annotation)) \
                              for p in params.args]
                ss[0].args = new_params
                new_returns = self.parse_type_annot(returns)
                ss[0].returns = new_returns
            else:
                new_params = params
                new_returns = returns
            for (x,t) in new_params:
                new_env[x] = t
            rt = self.type_check_stmts(body, new_env)
            self.check_type_equal(new_returns, rt, ss[0])
            return self.type_check_stmts(ss[1:], env)
          case ast.Return(value):
            return self.type_check_exp(value, env)
          case _:
            return super().type_check_stmts(ss, env)

    def type_check(self, p):
        match p:
            case ast.Module(body):
                env = {}
                for s in body:
                    match s:
                        case ast.FunctionDef(name, params, bod, dl, returns, comment):
                            # it is nessecary, that all functions always return something
                            if not (
                                returns or isinstance(bod[len(bod) - 1], ast.Return)
                            ):
                                bod.append(ast.Return(ast.Constant(None)))
                            if isinstance(params, ast.arguments):
                                params_t = [
                                    self.parse_type_annot(p.annotation)
                                    for p in params.args
                                ]
                            else:
                                params_t = [t for (x, t) in params]  # type: ignore
                            env[name] = utils.FunctionType(
                                params_t, self.parse_type_annot(returns)  # type: ignore
                            )
                self.type_check_stmts(body, env)
            case _:
                raise Exception(
                    "type_check: unexpected "
                    + repr(p)
                )
