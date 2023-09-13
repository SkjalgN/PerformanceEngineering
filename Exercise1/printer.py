
#
#Printer class----------------------------------------------------------------------
#

class Printer:

    def __init__(self, ship):
            self.ship = ship

    def get_ship(self):
        return self.ship
    
    def set_ship(self,ship):
        self.ship = ship

    def print_start(self):
        print("--------------------START OF PROGRAM--------------------")
        print("\n")
        print(f"Ship width,length,height: {self.ship.width},{self.ship.length*2},{self.ship.height}")
        print("\n")

    def print_end(self):
        print("--------------------END OF PROGRAM--------------------")

    def print_pause(self):
        print("\n")
        print("-------------------------------------------------------")
        print("\n")

    def print_ship(self):
        for section in self.get_ship().get_cargo():
            print(section)

    def print_sections(self):
        for x in self.get_ship().get_cargo():
            for section in x:
                print(section)
                for width in section.get_stacks():
                    for stack in width:
                        print("stack at " , stack.get_position() , " with " ,stack.get_stack_height(), " containers and weight", stack.get_stack_weight())
                print("\n")
            print("ship weight: ", self.get_ship().get_ship_weight(), " with ", self.get_ship().get_ship_containers(), " containers")

    def print_section(self,id):
        for x in self.get_ship().get_cargo():
            for section in x:
                if section.get_id() == id:
                    print(section)
                    for width in section.get_stacks():
                        for stack in width:
                            print("stack at " , stack.get_position() , " with " ,stack.get_stack_height(), " containers and weight", stack.get_stack_weight())
                    print("\n")

    def print_sections_operations(self):
        print("operations: ", self.get_ship().get_operations())
        print("load time one crane: ", self.get_ship().load_time_one_crane())
        print("load time three cranes: ", self.get_ship().load_time_three_cranes())
        print("\n")
        for x in self.get_ship().get_cargo():
            for section in x:
                print(section)
                print("operations: ", section.get_operations())

    def print_container_weight(self):
        for x in self.get_ship().get_cargo():
            for section in x:
                print(section)
                for width in section.get_stacks():
                    for stack in width:
                        stack1 = []
                        for container in stack.get_containers():
                            stack1.append(stack.get_list_weight(container))
                        print("stack at " , stack.get_position() , " with weights" ,stack1)
                print("\n")
        print("ship weight: ", self.get_ship().get_ship_weight(), " with ", self.ship.get_ship_containers(), " containers")
        print("starboard weight: ", self.get_ship().get_starboard_weight())
        print("port weight: ", self.get_ship().get_port_weight())
        print("bow weight: ", self.get_ship().get_bow_weight())
        print("mid weight: ", self.get_ship().get_mid_weight())
        print("stern weight: ", self.get_ship().get_stern_weight())

    def print_container_code(self):
        for x in self.get_ship().get_cargo():
            for section in x:
                print(section)
                for width in section.get_stacks():
                    for stack in width:
                        stack1 = []
                        for container in stack.get_containers():
                            for cont in container:
                                stack1.append(cont.get_code())
                        print("stack at " , stack.get_position() , " with codes" ,stack1)
                print("\n")
        print("ship weight: ", self.get_ship().get_ship_weight(), " with ", self.get_ship().get_lookup_len(), " containers")
        print("starboard weight: ", self.get_ship().get_starboard_weight())
        print("port weight: ", self.get_ship().get_port_weight())
        print("bow weight: ", self.get_ship().get_bow_weight())
        print("mid weight: ", self.get_ship().get_mid_weight())
        print("stern weight: ", self.get_ship().get_stern_weight())


    def print_containers_in_section(self,id):
        for x in self.get_ship().get_cargo():
            for section in x:
                if section.get_id() == id:
                    for width in section.get_stacks():
                        for stack in width:
                            for container in stack.get_containers():
                                print(container.get_code())

    
    def print_ship_visually(self):
        for x in self.get_ship().get_cargo():
            for section in x:
                print(section)
                for width in section.get_stacks():
                    for stack in width:
                        if stack.get_stack_height() == 10:
                            print(stack.get_stack_height(), end = " ")
                        else:
                            print(stack.get_stack_height(), end = "  ")
                    print("\n")
                print("\n")
            

def get_math(self):
    print("heriu")
