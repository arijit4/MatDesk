from constants import *
from error import InvalidSyntaxError
from nodes import *

class Parser:
    def __init__(self, tokens):
        self.current_tok = None
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok
    
    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            op_tok = tok
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error:
                return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "invalid usage of operator"))
            return res.success(UnaryOpNode(op_tok, factor))
        elif tok.type in (TT_INT, TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))
        elif tok.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_tok.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected ')'"))
        
        return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected a number"))
    
    def power(self):
        return self.bin_op(self.factor, (TT_POW,))
    
    def term(self):
        return self.bin_op(self.power, (TT_MUL, TT_DIV))


    def expr(self):
        # if  self.current_tok.matches(TT_KEYWORD, 'FOR'):
        #     return self.for_expr()
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        
        if res.error:
            return res
        
        while self.current_tok.type in ops:
            op_token = self.current_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error:
                return res
            left = BinOpNode(left, op_token, right)
        return res.success(left)
    
    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '+', '-', '*', '/'"
            ))
        return res

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    # def __repr__(self):
    #     return f'{self.node}'
    
    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error:
                self.error = res.error
            return res.node
        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self