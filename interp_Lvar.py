import ast
import utils
from interp_Lint import InterpLint


class InterpLvar(InterpLint):
    def interp_exp(self, e, env):
        match e:
            case ast.Name(id):
                return env[id]
            case _:
                return super().interp_exp(e, env)

    def interp_stmts(self, ss, env):
        if len(ss) == 0:
            return
        match ss[0]:
            case ast.Assign([lhs], value):
                env[lhs.id] = self.interp_exp(value, env)  # type: ignore
                return self.interp_stmts(ss[1:], env)
            case _:
                return super().interp_stmts(ss, env)

    def interp(self, p):
        match p:
            case ast.Module(body):
                self.interp_stmts(body, {})
            case _:
                raise Exception(
                    "interp: unexpected "
                    + repr(p)
                )


if __name__ == "__main__":
    eight = ast.Constant(8)
    neg_eight = ast.UnaryOp(ast.USub(), eight)
    read = ast.Call(ast.Name("input_int"), [])
    ast1_1 = ast.BinOp(read, ast.Add(), neg_eight)
    pr = ast.Expr(ast.Call(ast.Name("print"), [ast1_1]))
    p = ast.Module([pr])
    interp = InterpLvar()
    interp.interp(p)
