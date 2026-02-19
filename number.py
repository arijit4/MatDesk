from error import RTError

class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()

    def __repr__(self):
        return str(self.value)   

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
    
    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_pos(self.pos_start, other.pos_end), None
        else:
            raise Exception("Cannot add Number and " + str(type(other)) + " currently :)")
        
    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_pos(self.pos_start, other.pos_end), None
        else:
            raise Exception("Cannot subtract Number and " + str(type(other)) + " currently :)") 
        
    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_pos(self.pos_start, other.pos_end), None
        else:
            raise Exception("Cannot multiply Number and " + str(type(other)) + " currently :)")
    
    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(other.pos_start, other.pos_end, "division by zero")
            return Number(self.value / other.value).set_pos(self.pos_start, other.pos_end), None
        else:
            raise Exception("Cannot divide Number and " + str(type(other)) + " currently :)")
    
    def powed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_pos(self.pos_start, other.pos_end), None
        else:
            raise Exception("Cannot exponentiate Number and " + str(type(other)) + " currently :)")
        
              