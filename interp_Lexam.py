from ast import *
import math
from interp_Lfun import InterpLfun
from utils import *

class InterpLexam(InterpLfun):
  def interp_exp(self, e, env):
    match e:
      case AllocateArray(length, typ):  # FIXED
          length = self.interp_exp(length, env)
          return [None] * length
      case ast.List(es, ast.Load()):
          return [self.interp_exp(e, env) for e in es]
      case Subscript(tup, index, Load()):
          t = self.interp_exp(tup, env)
          n = self.interp_exp(index, env)
          if n >= 0 and n < len(t):
              return t[n]
          else:
              raise TrappedError('index out of bounds')
      case BinOp(left, Mult(), right):
          l = self.interp_exp(left, env); r = self.interp_exp(right, env)
          return l * r
      case BinOp(left, FloorDiv(), right):
          l = self.interp_exp(left, env); r = self.interp_exp(right, env)
          aq = abs(l) // abs(r)
          return aq if l * r >=0 else -aq
      case BinOp(left, Mod(), right):
          l = self.interp_exp(left, env); r = self.interp_exp(right, env)
          ar = abs(l) % abs(r)
          return ar if l >=0 else -ar
      case BinOp(left, LShift(), right):
          l = self.interp_exp(left, env); r = self.interp_exp(right,env)
          return l << r
      case BinOp(left, RShift(), right):
          l = self.interp_exp(left, env); r = self.interp_exp(right,env)
          return l >> r
      case BinOp(left, BitOr(), right):
          l = self.interp_exp(left, env); r = self.interp_exp(right, env)
          return l | r
      case BinOp(left, BitXor(), right):
          l = self.interp_exp(left, env); r = self.interp_exp(right,env)
          return l ^ r
      case BinOp(left, BitAnd(), right):
          l = self.interp_exp(left, env); r = self.interp_exp(right,env)
          return l & r
      case Call(Name('array_len'), [tup]):
        t = self.interp_exp(tup, env)
        return len(t)
      case Call(Name('array_load'), [tup, index]):
        t = self.interp_exp(tup, env)
        n = self.interp_exp(index, env)
        if n >= 0 and n < len(t):
            return t[n]
        else:
            raise TrappedError('array index out of bounds')
      case Call(Name('array_store'), [tup, index, value]):
        t = self.interp_exp(tup, env)
        n = self.interp_exp(index, env)
        if n >= 0 and n < len(t):
            t[n] = self.interp_exp(value, env)
        else:
            raise TrappedError('array index out of bounds')
        return None
      case _:
        return super().interp_exp(e, env)

  def interp_stmts(self, ss, env):
    if len(ss) == 0:
      return
    match ss[0]:
      case Assign([Subscript(lst, index, Store())], value):
        t = self.interp_exp(lst, env)
        n = self.interp_exp(index, env)
        if n >= 0 and n < len(t):
            t[n] = self.interp_exp(value, env)
        else:
            raise TrappedError('index out of bounds')
        return self.interp_stmts(ss[1:], env)
      case _:
        return super().interp_stmts(ss, env)
