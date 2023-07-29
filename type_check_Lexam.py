import ast
from types import NoneType
from type_check_Lfun import TypeCheckLfun
import utils


class TypeCheckLexam(TypeCheckLfun):
    def type_check_exp(self, e, env):
        match e:
            case utils.AllocateArray(length, typ):  # FIXED
                return typ
            case ast.List(es, ast.Load()):
                ts = [self.type_check_exp(e, env) for e in es]
                elt_ty = ts[0] if len(ts) > 0 else utils.Bottom()
                for (ty, elt) in zip(ts, es):
                    self.check_type_equal(elt_ty, ty, elt)
                e.has_type = utils.ListType(elt_ty)  # type: ignore
                return e.has_type  # type: ignore
            case ast.Call(ast.Name("len"), [tup]):
                tup_t = self.type_check_exp(tup, env)
                tup.has_type = tup_t  # type: ignore
                match tup_t:
                    case utils.ListType(_):
                        return utils.IntType()
                    case utils.Bottom():
                        return utils.Bottom()
                    case _:
                        return super().type_check_exp(e, env)
            case ast.Call(ast.Name("array_len"), [tup]):
                tup_t = self.type_check_exp(tup, env)
                tup.has_type = tup_t  # type: ignore
                match tup_t:
                    case utils.ListType(_):
                        return utils.IntType()
                    case _:
                        raise Exception(
                            "array_len expected list, not "
                            + repr(tup_t)
                        )
            case ast.Call(ast.Name("array_load"), [tup, index]):
                tup_ty = self.type_check_exp(tup, env)
                tup.has_type = tup_ty  # type: ignore
                index_ty = self.type_check_exp(index, env)
                self.check_type_equal(index_ty, utils.IntType(), index)
                match tup_ty:
                    case utils.ListType(t):
                        return t
                    case _:
                        raise Exception(
                            "array_len expected list, not "
                            + repr(tup_ty)
                        )
            case ast.Call(ast.Name("array_store"), [tup, index, value]):
                tup_ty = self.type_check_exp(tup, env)
                tup.has_type = tup_ty  # type: ignore
                index_ty = self.type_check_exp(index, env)
                value_ty = self.type_check_exp(value, env)
                self.check_type_equal(index_ty, utils.IntType(), index)
                match tup_ty:
                    case utils.ListType(t):
                        self.check_type_equal(value_ty, t, value)
                        return utils.VoidType()
                    case _:
                        raise Exception(
                            "array_store expected list, not "
                            + repr(tup_ty)
                        )
            case ast.Subscript(tup, index, ast.Load()):
                tup_ty = self.type_check_exp(tup, env)
                tup.has_type = tup_ty  # type: ignore
                index_ty = self.type_check_exp(index, env)
                self.check_type_equal(index_ty, utils.IntType(), index)
                match tup_ty:
                    case utils.ListType(ty):
                        return ty
                    case _:
                        return super().type_check_exp(e, env)
            case ast.BinOp(left, ast.Mult() | ast.FloorDiv() | ast.Mod(), right):
                l = self.type_check_exp(left, env)
                self.check_type_equal(l, utils.IntType(), left)
                r = self.type_check_exp(right, env)
                self.check_type_equal(r, utils.IntType(), right)
                return utils.IntType()
            case _:
                return super().type_check_exp(e, env)

    def type_check_stmts(self, ss, env):
        if len(ss) == 0:
            return
        match ss[0]:
            case ast.Assign([ast.Subscript(tup, index, ast.Store())], value):
                tup_ty = self.type_check_exp(tup, env)
                value_ty = self.type_check_exp(value, env)
                index_ty = self.type_check_exp(index, env)
                self.check_type_equal(index_ty, utils.IntType(), index)
                tup.has_type = tup_ty
                match tup_ty:
                    case utils.ListType(ty):
                        self.check_type_equal(ty, value_ty, ss[0])          
                    case utils.Bottom():
                        pass
                    case _:
                        return super().type_check_stmts(ss, env)
                return self.type_check_stmts(ss[1:], env)
            case _:
                return super().type_check_stmts(ss, env)
