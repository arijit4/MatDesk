from number import Number
from constants import *

class Interpreter:
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)
    
    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method defined')
    
    def visit_NumberNode(self, node):
        return RTResult().success(Number(node.tok.value).set_pos(node.tok.pos_start, node.tok.pos_end))
    
    def visit_BinOpNode(self, node):
        res = RTResult()
        left = res.register(self.visit(node.left_node))
        if res.error: return res
        right = res.register(self.visit(node.right_node))
        
        if res.error: return res
        
        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error =  left.multed_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_by(right)
        elif node.op_tok.type == TT_POW:
            result, error = left.powed_by(right)

        if error: return res.failure(error)
        return res.success(result.set_pos(node.op_tok.pos_start, right.pos_end))

    def visit_UnaryOpNode(self, node):
        res = RTResult()
        num = res.register(self.visit(node.node))
        if res.error: return res

        error = None

        if node.op_tok.type == TT_MINUS:
            num, error = Number(-num.value).set_pos(node.op_tok.pos_start, num.pos_end)
            if error: return res.failure(error)
            return res.success(num)
        elif node.op_tok.type == TT_PLUS:
            return num.set_pos(node.op_tok.pos_start, num.pos_end)
        

class RTResult:
    def __init__(self):
        self.value = None
        self.error = None
    
    def register(self, res):
        if res.error:
            self.error = res.error
        return res.value
    
    def success(self, value):
        self.value = value
        return self
    
    def failure(self, error):
        self.error = error
        return self