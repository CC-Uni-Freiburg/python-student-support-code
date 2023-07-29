import ast
from types import NoneType
import utils
import copy


class TypeCheckCif:
    def check_type_equal(self, t1, t2, e):
        if t1 == utils.Bottom() or t2 == utils.Bottom():
            pass
        elif t1 != t2:
            raise Exception(
                "error: "
                + repr(t1)
                + " != "
                + repr(t2)
                + " in "
                + repr(e)
            )

    def combine_types(self, t1, t2):
        match (t1, t2):
            case (utils.Bottom(), _):
                return t2
            case (_, utils.Bottom()):
                return t1
            case _:
                return t1

    def type_check_atm(self, e, env):
        match e:
            case ast.Name(id):
              t = env.get(id, utils.Bottom())
              env[id] = t  # make sure this gets into the environment for later definedness checking
              return t
            case ast.Constant(value) if isinstance(value, bool):
                return utils.BoolType()
            case ast.Constant(value) if isinstance(value, int):
                return utils.IntType()
            case ast.Constant(value) if isinstance(value, NoneType):
                return utils.VoidType()
            case _:
                raise Exception(
                    "error in type_check_atm, unexpected "
                    + repr(e)
                )

    def type_check_exp(self, e, env):
        match e:
            case ast.Name(id):
                return self.type_check_atm(e, env)
            case ast.Constant(value):
                return self.type_check_atm(e, env)
            case ast.IfExp(test, body, orelse):
                test_t = self.type_check_exp(test, env)
                self.check_type_equal(utils.BoolType(), test_t, test)
                body_t = self.type_check_exp(body, env)
                orelse_t = self.type_check_exp(orelse, env)
                self.check_type_equal(body_t, orelse_t, e)
                return body_t
            case ast.BinOp(left, op, right) if isinstance(op, ast.Add) or isinstance(
                op, ast.Sub
            ):
                l = self.type_check_atm(left, env)
                self.check_type_equal(l, utils.IntType(), e)
                r = self.type_check_atm(right, env)
                self.check_type_equal(r, utils.IntType(), e)
                return utils.IntType()
            case ast.UnaryOp(ast.USub(), v):
                t = self.type_check_atm(v, env)
                self.check_type_equal(t, utils.IntType(), e)
                return utils.IntType()
            case ast.UnaryOp(ast.Not(), v):
                t = self.type_check_exp(v, env)
                self.check_type_equal(t, utils.BoolType(), e)
                return utils.BoolType()
            case ast.Compare(left, [cmp], [right]) if isinstance(
                cmp, ast.Eq
            ) or isinstance(cmp, ast.NotEq):
                l = self.type_check_atm(left, env)
                r = self.type_check_atm(right, env)
                self.check_type_equal(l, r, e)
                return utils.BoolType()
            case ast.Compare(left, [cmp], [right]):
                l = self.type_check_atm(left, env)
                self.check_type_equal(l, utils.IntType(), left)
                r = self.type_check_atm(right, env)
                self.check_type_equal(r, utils.IntType(), right)
                return utils.BoolType()
            case ast.Call(ast.Name("input_int"), []):
                return utils.IntType()
            case utils.Begin(ss, e):
                self.type_check_stmts(ss, env)
                return self.type_check_exp(e, env)
            case _:
                raise Exception(
                    "error in type_check_exp, unexpected "
                    + repr(e)
                )

    def type_check_stmts(self, ss, env):
        for s in ss:
            self.type_check_stmt(s, env)

    def type_check_stmt(self, s, env):
        match s:
            case ast.Assign([lhs], value):
                t = self.type_check_exp(value, env)
                if lhs.id in env:  # type: ignore
                    lhs_ty = env.get(lhs.id, utils.Bottom())  # type: ignore
                    self.check_type_equal(lhs_ty, t, s)
                    env[lhs.id] = self.combine_types(t, lhs_ty)  # type: ignore
                else:
                    env[lhs.id] = t  # type: ignore
            case ast.Expr(ast.Call(ast.Name("print"), [arg])):
                t = self.type_check_exp(arg, env)
                self.check_type_equal(t, utils.IntType(), s)
            case ast.Expr(value):
                self.type_check_exp(value, env)
            case ast.If(ast.Compare(left, [cmp], [right]), body, orelse):
                left_t = self.type_check_atm(left, env)
                right_t = self.type_check_atm(right, env)
                self.check_type_equal(left_t, right_t, s)  # not quite strict enough
                self.type_check_stmts(body, env)
                self.type_check_stmts(orelse, env)
            case utils.Goto(label):
                pass
            case ast.Return(value):
                value_t = self.type_check_exp(value, env)
            case _:
                raise Exception(
                    "error in type_check_stmt, unexpected"
                    + repr(s)
                )

    def type_check(self, p):
        match p:
            case utils.CProgram(body):
                env = {}
                while True:
                    old_env = copy.deepcopy(env)
                    for (l, ss) in body.items():  # type: ignore
                        self.type_check_stmts(ss, env)
                    if env == old_env:
                        break
                p.var_types = env  # type: ignore
            case _:
                raise Exception("error in type_check, unexpected " + repr(p))
