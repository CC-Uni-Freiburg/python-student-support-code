import ast
from type_check_Lvar import TypeCheckLvar
import utils
from types import NoneType


class TypeCheckLif(TypeCheckLvar):
    def type_check_exp(self, e, env):
        match e:
            case ast.Constant(value) if isinstance(value, bool):
                return utils.BoolType()
            case ast.IfExp(test, body, orelse):
                test_t = self.type_check_exp(test, env)
                self.check_type_equal(utils.BoolType(), test_t, test)
                body_t = self.type_check_exp(body, env)
                orelse_t = self.type_check_exp(orelse, env)
                self.check_type_equal(body_t, orelse_t, e)
                # Return the most specialised type
                return body_t if isinstance(orelse_t, utils.Bottom) else orelse_t
            case ast.BinOp(left, ast.Sub(), right):
                l = self.type_check_exp(left, env)
                self.check_type_equal(l, utils.IntType(), left)
                r = self.type_check_exp(right, env)
                self.check_type_equal(r, utils.IntType(), right)
                return utils.IntType()
            case ast.UnaryOp(ast.Not(), v):
                t = self.type_check_exp(v, env)
                self.check_type_equal(t, utils.BoolType(), v)
                return utils.BoolType()
            case ast.BoolOp(op, values):
                left = values[0]
                right = values[1]
                l = self.type_check_exp(left, env)
                self.check_type_equal(l, utils.BoolType(), left)
                r = self.type_check_exp(right, env)
                self.check_type_equal(r, utils.BoolType(), right)
                return utils.BoolType()
            case ast.Compare(left, [cmp], [right]) if isinstance(cmp, ast.Eq) or isinstance(
                cmp, ast.NotEq
            ):
                l = self.type_check_exp(left, env)
                r = self.type_check_exp(right, env)
                self.check_type_equal(l, r, e)
                return utils.BoolType()
            case ast.Compare(left, [cmp], [right]):
                l = self.type_check_exp(left, env)
                self.check_type_equal(l, utils.IntType(), left)
                r = self.type_check_exp(right, env)
                self.check_type_equal(r, utils.IntType(), right)
                return utils.BoolType()
            case utils.Begin(ss, e):
                self.type_check_stmts(ss, env)
                return self.type_check_exp(e, env)
            case _:
                return super().type_check_exp(e, env)

    def type_check_stmts(self, ss, env):
        if len(ss) == 0:
            return
        match ss[0]:
            case ast.If(test, body, orelse):
                test_t = self.type_check_exp(test, env)
                self.check_type_equal(utils.BoolType(), test_t, test)
                body_t = self.type_check_stmts(body, env)
                orelse_t = self.type_check_stmts(orelse, env)
                cont_t = self.type_check_stmts(ss[1:], env)
                check_equal = []
                # Gather the returned types of both branches and the continuation
                if not isinstance(body_t, NoneType):
                    check_equal.append(body_t)
                if not isinstance(orelse_t, NoneType):
                    check_equal.append(orelse_t)
                if not isinstance(cont_t, NoneType):
                    check_equal.append(cont_t)
                # Check all returned types equal and return the most specialised
                if len(check_equal) > 1:
                    self.check_type_equal(check_equal[0], check_equal[1], ss)
                if len(check_equal) > 2:
                    self.check_type_equal(check_equal[1], check_equal[2], ss)
                ret_t = check_equal[0] if len(check_equal) > 0 else None
                for t in check_equal:
                    if not isinstance(t, utils.Bottom):
                        ret_t = t
                        break
                return ret_t
            case _:
                return super().type_check_stmts(ss, env)
