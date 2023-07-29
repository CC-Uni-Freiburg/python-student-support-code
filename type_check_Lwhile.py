import ast
from types import NoneType
from type_check_Lif import TypeCheckLif
import utils
from types import NoneType


class TypeCheckLwhile(TypeCheckLif):
  def type_check_stmts(self, ss, env):
    if len(ss) == 0:
      return
    match ss[0]:
      case ast.While(test, body, []):
        test_t = self.type_check_exp(test, env)
        self.check_type_equal(utils.BoolType(), test_t, test)
        body_t = self.type_check_stmts(body, env)
        ret_t = self.type_check_stmts(ss[1:], env)
        check_equal = []
        # Gather the returned types
        if not isinstance(body_t, NoneType):
          check_equal.append(body_t)
        if not isinstance(ret_t, NoneType):
          check_equal.append(ret_t)
        # Check all returned types equal and return the most specialised
        if len(check_equal) > 1:
          self.check_type_equal(check_equal[0], check_equal[1], ss)
          return check_equal[0] if isinstance(check_equal[1], utils.Bottom) else check_equal[1]
        return check_equal[0] if len(check_equal) > 0 else None
      case _:
        return super().type_check_stmts(ss, env)
