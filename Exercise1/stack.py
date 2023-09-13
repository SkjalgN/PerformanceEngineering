#
#Stack Class-------------------------------------------------------------------------------------------------
#

class Stack:
    def __init__(self, x,y):
        self.position = [x,y]
        self.containers = []
        self.stacktemp = []
        self.full = False
        self.empty = True
        self.operations = 0

    def __repr__(self):
        return f"Stack(position: {self.position},  containers: {self.containers})"
    
    #
    #Getters and Setters--------------------------------------------------------------------------------------
    #

    def get_position(self):
        return self.position
    
    def get_top_container(self):
        if self.containers:
            return self.containers[-1]
        
    def get_containers(self):
        return self.containers
    
    def get_full(self):
        return self.full
    
    def get_empty(self):
        return self.empty
    
    def get_stacktemp(self):
        return self.stacktemp
    
    def get_stack_height(self):
        return len(self.containers)   
    
    def get_operations(self):
        return self.operations

    def set_position(self,x,y,z):
        self.position[0] = x
        self.position[1] = y
        self.position[2] = z

    def set_containers(self,containers):
        self.containers = containers

    def set_full(self,full):
        self.full = full

    def set_empty(self,empty):
        self.empty = empty

    def set_stacktemp(self,stacktemp):
        self.stacktemp = stacktemp

    def set_operations(self,operations):
        self.operations = operations

    #
    #Functions------------------------------------------------------------------------------------------------
    #

    def get_stack_weight(self):
        weight = 0
        for list in self.get_containers():
            for container in list:
                weight += container.get_total_weight()
        return weight

    def get_list_weight(self,list):
        weight = 0
        for container in list:
            weight += container.get_total_weight()
        return weight


    def load_to_stack(self,container,section,ship):
        loaded = False
        while not loaded:
            if not self.get_containers():
                self.containers.append(container)
                loaded = True
            elif self.get_list_weight(self.get_containers()[-1]) >= self.get_list_weight(container):
                self.get_containers().append(container)
                loaded = True
            elif self.get_list_weight(self.get_containers()[-1]) < self.get_list_weight(container):
                self.get_stacktemp().append(self.get_containers().pop())
        for i in range(len(self.get_stacktemp())):
            self.get_containers().append(self.get_stacktemp().pop())
        ship.add_container_to_lookup(container)
        if self.get_stack_height() >= ship.get_height():
            self.set_full(True)
        self.set_empty(False)
        section.set_empty(False)
        ship.set_empty(False)
        self.operations += 1

    def unload_from_stack(self,section,ship):
        container = self.get_containers().pop()
        if self.get_stack_height() == 0:
            self.set_empty(True)
        self.set_full(False)
        section.set_full(False)
        ship.set_full(False)
        for cont in container:
            ship.remove_container_from_lookup(cont.get_code())
        self.operations += 1

    def unload_from_stack_by_id(self,list,section,ship):
        unloaded = False
        while not unloaded:
            for container in self.get_containers()[-1]:
                print(list,container)
                if list == [container]:
                    self.get_containers().pop()
                    unloaded = True
                    break
                else:
                    self.stacktemp.append(self.get_containers().pop())
        for i in range(len(self.get_stacktemp())):
            self.get_containers().append(self.get_stacktemp().pop())
        if self.get_stack_height() == 0:
            self.set_empty(True)  
        self.set_full(False)
        section.set_full(False)
        ship.set_full(False)
        for container in list:
            ship.remove_container_from_lookup(container.get_code())  
        self.operations += 1

    def reset_operations(self):
        self.set_operations(0)