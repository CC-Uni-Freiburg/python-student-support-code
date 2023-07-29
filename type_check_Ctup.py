import ast
from type_check_Cwhile import TypeCheckCwhile
import utils


class TypeCheckCtup(TypeCheckCwhile):
    def check_type_equal(self, t1, t2, e):
        match t1:
            case utils.TupleType(ts1):
                match t2:
                    case utils.TupleType(ts2):
                        for (ty1, ty2) in zip(ts1, ts2):
                            self.check_type_equal(ty1, ty2, e)
                    case utils.Bottom():
                        pass
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
            case utils.Allocate(length, typ):
                return typ
            case utils.GlobalValue(name):
                return utils.IntType()
            case ast.Subscript(tup, ast.Constant(index), ast.Load()):
                tup_t = self.type_check_atm(tup, env)
                match tup_t:
                    case utils.TupleType(ts):
                        return ts[index]
                    case utils.Bottom():
                        return utils.Bottom()
                    case _:
                        raise Exception(
                            "type_check_exp: unexpected "
                            + repr(tup_t)
                        )
            case ast.Call(ast.Name("len"), [tup]):
                tup_t = self.type_check_atm(tup, env)
                match tup_t:
                    case utils.TupleType(ts):
                        return utils.IntType()
                    case utils.Bottom():
                        return utils.Bottom()
                    case _:
                        raise Exception(
                            "type_check_exp: unexpected "
                            + repr(tup_t)
                        )
            case _:
                return super().type_check_exp(e, env)

    def type_check_stmt(self, s, env):
        match s:
            case utils.Collect(size):
                pass
            case ast.Assign(
                [ast.Subscript(tup, ast.Constant(index), ast.Store())], value
            ):
                tup_t = self.type_check_atm(tup, env)
                value_t = self.type_check_atm(value, env)
                match tup_t:
                    case utils.TupleType(ts):
                        self.check_type_equal(ts[index], value_t, s)
                    case utils.Bottom():
                        pass
                    case _:
                        raise Exception(
                            "type_check_stmt: unexpected "
                            + repr(tup_t)
                        )
            case _:
                return super().type_check_stmt(s, env)
