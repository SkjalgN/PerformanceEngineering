
#Imports
import random

#
#Container class---------------------------------------------------------------
# 

class Container:

    CodeNumber = 100    

    def __init__(self,code,length,load):
            if length == 20 and 0 <= load <= 20:
                self.weight = 2
            elif length == 40 and 0 <= load <= 22:
                self.weight = 4
            else: 
                raise ValueError("length must be 20 and load 0-20 or length must be 40 and load 0-22")
            self.code = code
            self.length = length
            self.load = load
            self.totalweight =self.load + self.weight
            self.position = [None,None,None]

    @classmethod
    def create_small_container(cls,code,load):
        return cls(code,20,load)

    @classmethod
    def create_large_container(cls,code,load):
        return cls(code,40,load)

    @classmethod
    def create_random_container(cls):

        var = random.randint(1,2)
        Container.CodeNumber += 1
        if(var == 1):
            return Container.create_small_container(Container.CodeNumber,random.randint(0,20))
        else:
            return Container.create_large_container(Container.CodeNumber,random.randint(0,22))

    def __lt__(self, other):
        if self.weight == other.weight:
            return self.code < other.code
        return self.weight < other.weight

    def __repr__(self):
        return f"Container(code: {self.get_code()}, weight: {self.get_total_weight()})"

    #
    #Getters and Setters-----------------------------------------------------------
    #

    def get_code(self):
        return self.code

    def get_length(self):
        return self.length

    def get_weight(self):
        return self.weight

    def get_load(self):
        return self.load

    def get_total_weight(self):
        return self.totalweight

    def get_position(self):
        return self.position


    def set_code(self,code):
        self.code = code

    def set_length(self,length):
        self.length = length

    def set_weight(self,weight):
        self.weight = weight

    def set_load(self,load):
        self.load = load

    def set_position(self,x,y,z):
        self.position[0] = x
        self.position[1] = y
        self.position[2] = z


        
    
    
