import ast
from interp_Cif import InterpCif
from utils import *


class InterpCtup(InterpCif):
    def interp_cmp(self, cmp):
        match cmp:
            case ast.Is():
                return lambda x, y: x is y
            case _:
                return super().interp_cmp(cmp)

    def interp_exp(self, e, env):
        match e:
            case ast.Tuple(es, ast.Load()):
                return tuple([self.interp_exp(e, env) for e in es])
            case ast.Subscript(tup, Constant(index), ast.Load()):
                t = self.interp_exp(tup, env)
                if index >= 0 and index < len(t):
                    return t[index]
                else:
                    raise TrappedError('index out of bounds')
            case Allocate(length, typ):
                array = [None] * length
                return array
            case Begin(ss, e):
                self.interp_stmts(ss, env)
                return self.interp_exp(e, env)
            case GlobalValue(name):
                return 0  # bogus
            case ast.Call(ast.Name("len"), [tup]):
                t = self.interp_exp(tup, env)
                return len(t)
            case _:
                return super().interp_exp(e, env)

    def interp_stmts(self, ss, env):
        if len(ss) == 0:
            return
        match ss[0]:
            case Collect(size):
                return self.interp_stmts(ss[1:], env)
            case ast.Assign([ast.Subscript(tup, Constant(index), Store())], value):
                tup = self.interp_exp(tup, env)
                if index >= 0 and index < len(tup):
                    tup[index] = self.interp_exp(value, env)
                else:
                    raise TrappedError('index out of bounds')
                return self.interp_stmts(ss[1:], env)
            case _:
                return super().interp_stmts(ss, env)
