import ast
from interp_Lif import InterpLif
import utils


class InterpCif(InterpLif):
    def interp_stmts(self, ss, env):
        if len(ss) == 0:
            return
        match ss[0]:
            case ast.Return(value):
                return ast.Return(self.interp_exp(value, env))
            case utils.Goto(label):
                return utils.Goto(label)
            case _:
                return super().interp_stmts(ss, env)

    def interp(self, p):
        match p:
            case utils.CProgram(blocks):
                env = {}
                self.blocks = blocks
                r = self.interp_stmts(blocks[utils.label_name("start")], env)
                while isinstance(r, utils.Goto):
                    r = self.interp_stmts(self.blocks[utils.label_name(r.label)], env)
            case _:
                raise Exception(
                    "interp: unexpected "
                    + repr(p)
                )
