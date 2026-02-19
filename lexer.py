from token import Token
from position import Position
from error import IllegalCharError, InvalidSyntaxError
from constants import *

class Lexer:
    def __init__(self, fn, text):
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        if self.pos.idx < len(self.text):
            self.current_char = self.text[self.pos.idx]
        else:
            self.current_char = None

    def make_tokens(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                number = self.make_number()

                if isinstance(number, InvalidSyntaxError):
                    return [], number
                
                tokens.append(number)
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, '+', pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, '-', pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, '*', pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, '/', pos_start=self.pos))
                self.advance()
            elif self.current_char == '^':
                tokens.append(Token(TT_POW, '^', pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, '(', pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, ')', pos_start=self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")
        tokens.append(Token(TT_EOF, None, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        while self.current_char is not None and (self.current_char in DIGITS or self.current_char == '.'):
            if self.current_char == '.':
                if dot_count == 1:
                    # break
                    return InvalidSyntaxError(self.pos, self.pos, "too many dots in number")
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start=self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start=self.pos)
        