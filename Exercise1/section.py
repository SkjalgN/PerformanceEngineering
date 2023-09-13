
#
#Imports---------------------------------------------------------------------------------------------------
#

from stack import Stack

#
#Section Class-----------------------------------------------------------------------------------------------
#

class Section:
    def __init__(self,id,position):
        self.id = id
        self.position = [int(position[0]),int(position[1]),int(position[2]),int(position[3])]
        self.width = int(self.get_position()[1]-self.get_position()[0])
        self.length = int(self.get_position()[3]-self.get_position()[2])
        self.stacks = [[0]*int(self.length) for _ in range(int(self.width))]
        self.full = False
        self.empty = True
        self.availablestacks = []
        self.nonemptystacks = []
        self.operations = 0
        self.add_stacks()

    def __repr__(self):
        return f"Section(id: {self.id}, position: {self.position}, stacks: {self.get_number_of_stacks()})  weight: {self.get_section_weight()} and containers: {self.get_section_containers()}"
    
    #
    #Getters and Setters-------------------------------------------------------------------------------------
    #

    def get_id(self):
        return self.id
    
    def get_position(self):
        return self.position
    
    def get_stacks(self):
        return self.stacks
    
    def get_length(self):
        return self.length
    
    def get_width(self):
        return self.width
    
    def get_full(self):
        return self.full
    
    def get_empty(self):   
        return self.empty
    
    def get_availablestacks(self):
        return self.availablestacks
    
    def get_nonemptystacks(self):
        return self.nonemptystacks
    
    def get_operations(self):
        return self.operations
    

    def set_id(self,id):
        self.id = id

    def set_position(self,x1,x2,y1,y2):
        self.position[0] = x1
        self.position[1] = x2
        self.position[2] = y1
        self.position[3] = y2

    def set_stacks(self,stacks):
        self.stacks = stacks

    def set_full(self,full):
        self.full = full

    def set_empty(self,empty):
        self.empty = empty

    def set_availablestacks(self,availablestacks):
        self.availablestacks = availablestacks

    def set_nonemptystacks(self,nonemptystacks):
        self.nonemptystacks = nonemptystacks

    def set_operations(self,operations):
        self.operations = operations
    

    #
    #Section Commands----------------------------------------------------------------------------------
    #

    def get_number_of_stacks(self):
        return self.length*self.width
    
    def get_section_weight(self):
        weight = 0
        for x in range(self.get_width()):
            for y in range(self.get_length()):
                weight += self.stacks[x][y].get_stack_weight()
        return weight
    
    def get_section_containers(self):
        containers = 0
        for x in self.get_stacks():
            for stack in x:
                for list in stack.get_containers():
                    containers += len(list)
        return containers

    def add_stacks(self):
        for x in range(self.width):
            for y in range(self.length):
                stack = Stack(x,y)
                self.stacks[x][y] = stack
                self.get_availablestacks().append(stack)

    def check_available_stacks(self):
        self.set_availablestacks([])
        self.set_nonemptystacks([])
        for x in self.get_stacks():
            for stack in x:
                if not stack.get_full():
                    self.get_availablestacks().append(stack)
                if not stack.get_empty():
                    self.get_nonemptystacks().append(stack)
        if self.get_availablestacks() == []:
            self.set_full(True)
        else:
            self.set_full(False)
        if self.get_nonemptystacks() == []:
            self.set_empty(True)
        else:
            self.set_empty(False)
    
    def get_lightest_stack(self):
        self.check_available_stacks()
        if self.get_full():
            return None
        lightest = self.availablestacks[0]
        for stack in self.get_availablestacks():
                if stack.get_stack_weight() < lightest.get_stack_weight():
                    lightest = stack
        return lightest
    
    def get_heaviest_stack(self):
        self.check_available_stacks()
        if self.get_empty():
            return None
        heaviest = self.nonemptystacks[0]
        for stack in self.get_nonemptystacks():
                if stack.get_stack_weight() > heaviest.get_stack_weight():
                    heaviest = stack
        return heaviest
    
    def load_to_section(self,container,ship):
        self.check_available_stacks()
        if self.get_lightest_stack() == None:
            return None
        self.get_lightest_stack().load_to_stack(container,self,ship)
        self.operations += 1

    def unload_from_section(self,ship):
        self.check_available_stacks()
        if self.get_heaviest_stack() == None:
            return None
        self.get_heaviest_stack().unload_from_stack(self,ship)
        self.operations += 1

    def unload_from_section_by_id(self,container,ship):
        for x in self.stacks:
            for stack in x:
                for list in stack.get_containers():
                    if container in list:
                        stack.unload_from_stack_by_id(list,self,ship)
                        self.operations += 1
                        return True
                    
    def reset_operations(self):
        self.set_operations(0)

