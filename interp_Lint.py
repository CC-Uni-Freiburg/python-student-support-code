import ast
import utils


def interp_exp(e):
    match e:
        case ast.BinOp(left, ast.Add(), right):
            l = interp_exp(left)
            r = interp_exp(right)
            return l + r
        case ast.BinOp(left, ast.Sub(), right):
            l = interp_exp(left)
            r = interp_exp(right)
            return l - r
        case ast.UnaryOp(ast.USub(), v):
            return -interp_exp(v)
        case ast.Constant(value):
            return value
        case ast.Call(ast.Name("input_int"), []):
            return int(input())
        case _:
            raise Exception(
                "error in interp_exp, unexpected "
                + repr(e)
            )

def interp_stmt(s):
    match s:
        case ast.Expr(ast.Call(ast.Name("print"), [arg])):
            print(interp_exp(arg))
        case ast.Expr(value):
            interp_exp(value)
        case _:
            raise Exception(
                "error in interp_stmt, unexpected "
                + repr(s)
            )

def interp(p):
    match p:
        case ast.Module(body):
            for s in body:
                interp_stmt(s)
        case _:
            raise Exception(
                "error in interp, unexpected "
                + repr(p)
            )


# This version is for InterpLvar to inherit from
class InterpLint:
    def interp_exp(self, e, env):
        match e:
            case ast.BinOp(left, ast.Add(), right):
                l = self.interp_exp(left, env)
                r = self.interp_exp(right, env)
                return l + r
            case ast.BinOp(left, ast.Sub(), right):
                l = self.interp_exp(left, env)
                r = self.interp_exp(right, env)
                return l - r
            case ast.UnaryOp(ast.USub(), v):
                return -self.interp_exp(v, env)
            case ast.Constant(value):
                return value
            case ast.Call(ast.Name("input_int"), []):
                return int(input())
            case _:
                raise Exception(
                    "error in interp_exp, unexpected "
                    + repr(e)
                )

    def interp_stmts(self, ss, env):
        if len(ss) == 0:
            return
        match ss[0]:
            case ast.Expr(ast.Call(ast.Name("print"), [arg])):
                val = self.interp_exp(arg, env)
                print(val, end="")
                return self.interp_stmts(ss[1:], env)
            case ast.Expr(value):
                self.interp_exp(value, env)
                return self.interp_stmts(ss[1:], env)
            case _:
                raise Exception(
                    "error in interp_stmts, unexpected "
                    + repr(ss[0])
                )

    def interp(self, p):
        match p:
            case ast.Module(body):
                self.interp_stmts(body, {})
            case _:
                raise Exception(
                    "error in interp, unexpected "
                    + repr(p)
                )


if __name__ == "__main__":
    eight = ast.Constant(8)
    neg_eight = ast.UnaryOp(ast.USub(), eight)
    read = ast.Call(ast.Name("input_int"), [])
    ast1_1 = ast.BinOp(read, ast.Add(), neg_eight)
    pr = ast.Expr(ast.Call(ast.Name("print"), [ast1_1]))
    p = ast.Module([pr])
    interp(p)
