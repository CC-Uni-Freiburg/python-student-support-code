import ast
from types import NoneType
import utils


class TypeCheckLvar:
    def check_type_equal(self, t1, t2, e):
        if t1 != t2:
            raise Exception(
                "error: "
                + repr(t1)
                + " != "
                + repr(t2)
                + " in "
                + repr(e)
            )

    def type_check_exp(self, e, env):
        match e:
            case ast.BinOp(left, ast.Add(), right):
                l = self.type_check_exp(left, env)
                self.check_type_equal(l, utils.IntType(), left)
                r = self.type_check_exp(right, env)
                self.check_type_equal(r, utils.IntType(), right)
                return utils.IntType()
            case ast.BinOp(left, ast.Sub(), right):
                l = self.type_check_exp(left, env)
                self.check_type_equal(l, utils.IntType(), left)
                r = self.type_check_exp(right, env)
                self.check_type_equal(r, utils.IntType(), right)
                return utils.IntType()
            case ast.UnaryOp(ast.USub(), v):
                t = self.type_check_exp(v, env)
                self.check_type_equal(t, utils.IntType(), v)
                return utils.IntType()
            case ast.Name(id):
                return env[id]
            case ast.Constant(value) if isinstance(value, int):
                return utils.IntType()
            case ast.Constant(value) if isinstance(value, NoneType):
                return utils.VoidType()
            case ast.Call(ast.Name("input_int"), []):
                return utils.IntType()
            case _:
                raise Exception(
                    "type_check_exp: unexpected "
                    + repr(e)
                )

    def type_check_stmts(self, ss, env):
      if len(ss) == 0:
        return
      match ss[0]:
        case ast.Assign([ast.Name(id)], value):
          t = self.type_check_exp(value, env)
          if id in env:
            self.check_type_equal(env[id], t, value)
          else:
            env[id] = t
          return self.type_check_stmts(ss[1:], env)
        case ast.Expr(ast.Call(ast.Name('print'), [arg])):
          t = self.type_check_exp(arg, env)
          self.check_type_equal(t, utils.IntType(), arg)
          return self.type_check_stmts(ss[1:], env)
        case ast.Expr(value):
          self.type_check_exp(value, env)
          return self.type_check_stmts(ss[1:], env)
        case _:
          raise Exception(
              "type_check_stmts: unexpected "
              + repr(ss[0])
          )

    def type_check(self, p):
        match p:
            case ast.Module(body):
                self.type_check_stmts(body, {})
