#
#imports------------------------------------------------------------------------------------------------------
#

from container import Container
from section import Section
from printer import Printer


#
#Ship Class--------------------------------------------------------------------------------------------------
#

class Ship:

    def __init__(self,width,length,height):
        if (width % 2 == 0 and length % 6 == 0):
            self.width = int(width)
            self.length = int(length/2)
            self.height = int(height)
            self.cargo = [[0]*int(3) for _ in range(int(2))]
            self.temp = []
            self.lookup = {}
            self.availablesections = []
            self.nonemptysections = []
            self.operations = 0
            self.create_cargo()
            self.full = False
            self.empty = True
        else:  
            raise ValueError("width must be % 2 and length must be % 6")

    def create_cargo(self):
        x = 0
        y = 0
        id = 1
        for xpos in range(2):
            for ypos in range(3):
                newsection = Section(id,[x,x+self.width/2,y,y+self.length/3])
                self.cargo[xpos][ypos] = newsection
                self.get_available_sections().append(newsection)
                y += int(self.length/3)
                id += 1
            x += int(self.width/2)
            y = 0
            
    def __repr__(self):
        section_repr = '\n'.join(repr(section) for section in self.cargo)
        return 'Ship with containers:\n{}'.format(section_repr)


    #
    #Getters and Setters-------------------------------------------------------------------------------------
    #

    def get_width(self):
        return self.width

    def get_length(self):
        return self.length

    def get_height(self):
        return self.height

    def get_cargo(self):
        return self.cargo
    
    def get_temp(self):
        return self.temp

    def get_lookup(self):
        return self.lookup
    
    def get_section(self,id):
        for x in self.get_cargo():
            for section in x:
                if section.get_id() == id:
                    return section
        
    def get_available_sections(self):
        return self.availablesections
    
    def get_nonempty_sections(self):
        return self.nonemptysections
    
    def get_full(self):
        return self.full
    
    def get_empty(self):
        return self.empty
    
    def get_operations(self):
        return self.operations
            
    def set_width(self,width):
        self.width = width

    def set_length(self,length):
        self.length = length

    def set_height(self,height):
        self.height = height

    def set_containers(self,containers):
        self.cargo = containers

    def set_temp(self,temp):
        self.temp = temp
    
    def set_lookup(self,lookup):
        self.lookup = lookup

    def set_available_sections(self,availablesections):
        self.availablesections = availablesections
    
    def set_nonempty_sections(self,nonemptysections):
        self.nonemptysections = nonemptysections

    def set_full(self,full):
        self.full = full

    def set_empty(self,empty):
        self.empty = empty

    def set_operations(self,operations):
        self.operations = operations
    
    #
    #Dictionary Commands--------------------------------------------------------------------------------------
    #                   

    def add_container_to_lookup(self, container):
        for cont in container:
            self.lookup[cont.get_code()] = cont

    def remove_container_from_lookup(self, code):
        if code in self.get_lookup():
            del self.lookup[code]
        else:
            print("Container not found")
   
    def find_container_in_lookup(self, code):
        if code in self.get_lookup():
            return self.lookup[code]
        else:
            print("Container not found")
    
    def get_lookup_as_list(self):
        containers = list(self.get_lookup().values())
        return containers

    def get_lookup_len(self):
        return len(self.get_lookup())


    #
    #Ship Commands------------------------------------------------------------------------------------------
    #

    def get_section_by_id(self,id):
        for section in self.get_cargo():
            if section.get_id() == id:
                return section

    def reset_operations(self):
        self.operations = 0
        for x in self.get_cargo():
            for section in x:
                section.reset_operations()
                for x in section.get_stacks():
                    for stack in x:
                        stack.reset_operations()

    def random_set_of_containers(self,amount):
        containers = []
        for i in range(amount):
            containers.append(Container.create_random_container())
        return containers

    def load_containers(self,containers):
        for container in containers:
            self.check_available_sections()
            if self.full:
                print(f"{self.get_ship_containers()} containers loaded to ship in {self.get_operations()} operations")
                print("\n")
                return "Ship is full"
            self.load_container(container)
        print(f"{len(containers)} containers loaded to ship in {self.get_operations()} operations")
        print("\n")

    def load_container(self,container):
        newcontainer = []
        if container.get_length() == 20:
            if len(self.get_temp()) == 0:
                self.get_temp().append(container)
                return
            else:
                self.temp.append(container)
                newcontainer = self.get_temp()
                self.set_temp([])
        else:
            newcontainer = [container]    
        self.get_lightest_section().load_to_section(newcontainer,self)
        self.operations += 1

    def unload_containers(self):
        while not self.get_empty() :
            self.unload_container()
        print(f"containers unloaded from ship in {self.operations} operations")
        print("\n")

    def unload_container(self):
        self.check_available_sections()
        if self.get_empty():
            return None
        else:
            self.get_heaviest_section().unload_from_section(self)
            self.operations += 1

    def unload_container_by_id(self,code):
        container = self.find_container_in_lookup(code)
        for x in self.get_cargo():
            for section in x:
                if section.unload_from_section(container,self):
                    self.operations += 1
                    return
        print("Container not found")

    def check_available_sections(self):
        self.set_available_sections([])
        self.set_nonempty_sections([])
        for x in self.get_cargo():
            for section in x:
                if not section.get_full():
                    self.get_available_sections().append(section)
                if not section.get_empty():
                    self.get_nonempty_sections().append(section)
        if self.get_available_sections() == []:
            self.set_full(True)
        else:
            self.set_full(False)
        if self.get_nonempty_sections() == []:
            self.set_empty(True)
        else:  
            self.set_empty(False)

    def get_lightest_section(self):
        lightest = self.availablesections[0]
        for section in self.get_available_sections():
                if section.get_section_weight() < lightest.get_section_weight():
                    lightest = section
        return lightest

    def get_heaviest_section(self):
        heaviest = self.nonemptysections[0]
        for section in self.get_nonempty_sections():
                if section.get_section_weight() > heaviest.get_section_weight():
                    heaviest = section
        return heaviest
    
    #
    #Weight calculations -----------------------------------------------------------------------------------------
    #
    
    def get_ship_weight(self):
        weight = 0
        for x in self.get_cargo():
            for section in x:
                weight += section.get_section_weight()
        return weight
    
    def get_ship_containers(self):
        containers = 0
        for x in self.get_cargo():
            for section in x:
                containers += section.get_section_containers()
        return containers

    def get_starboard_weight(self):
        weight = 0
        for x in self.cargo[0]:
            weight += x.get_section_weight()
        return weight
    
    def get_port_weight(self):
        weight = 0
        for x in self.cargo[1]:
            weight += x.get_section_weight()
        return weight
    
    def get_bow_weight(self):
        weight = 0
        for x in self.get_cargo():
            weight += x[0].get_section_weight()
        return weight
    
    def get_mid_weight(self):
        weight = 0
        for x in self.get_cargo():
            weight += x[1].get_section_weight()
        return weight
    
    def get_stern_weight(self):
        weight = 0
        for x in self.get_cargo():
            weight += x[2].get_section_weight()
        return weight
        
    def is_balanced(self,x,y):
        balanced = True
        if self.get_starboard_weight() > x*self.get_port_weight() or self.get_starboard_weight()*x < self.get_port_weight():
            balanced = False
            print("feil 1")
        for x in self.get_cargo():
            for section1 in x:
                for section2 in x:
                    if section2.get_section_weight() > y*section1.get_section_weight():
                        balanced = False
                        print("feil 2")
                    if section2.get_section_weight()*y < section1.get_section_weight():
                        balanced = False
                        print("feil 3")
        container = None
        for x in self.get_cargo():
            for section in x:
                for x in section.get_stacks():
                    for stack in x:
                        for i in stack.get_containers():
                            if container == None:
                                container = i
                            elif stack.get_list_weight(container) < stack.get_list_weight(i):
                                balanced = False
                                print("feil 4",stack.get_position())
                        container = None
        return balanced
    
    #
    #Crane calculations -----------------------------------------------------------------------------------------
    #
    
    def load_time_one_crane(self):
        time = 0
        time += self.get_operations() * 4
        return time
    
    def load_time_three_cranes(self):
        time = 0
        time1 = self.get_section(1).get_operations() * 4 + self.get_section(4).get_operations() * 4
        time2 = self.get_section(2).get_operations() * 4 + self.get_section(5).get_operations() * 4
        time3 = self.get_section(3).get_operations() * 4 + self.get_section(6).get_operations() * 4
        time += max(time1,time2,time3)
        return time
    
    #
    #Save and Load to File--------------------------------------------------------------------------------------
    #

    def clear_file(self):
        with open('textfile.tsv','w') as f:
            f.write('')

    def save_to_file(self):
        self.clear_file()
        with open('textfile.tsv', "a") as f:
            for i in self.get_lookup_as_list():
                if(i != 0):
                    f.write(f"{i.get_code()}\t{i.get_length()}\t{i.get_weight()}\t{i.get_load()}\n")
    
    def load_from_file(self):
        containers = []
        with open('textfile.tsv', 'r') as file:
            for line in file:
                container_data = line.strip().split('\t')
                code, length, weight, load = container_data
                container = Container(int(code), int(length), int(load))
                containers.append(container)
        return containers
    
    def load_ship_from_file(self):
        self.load_containers(self.load_from_file())
                    

#
# Main ----------------------------------------------------------------------------------------------------------
#    

def main():
    ship1 = Ship(10, 12, 10)
    printer = Printer(ship1)
    printer.print_start()
    ship1.load_containers(ship1.random_set_of_containers(12300))
    printer.print_container_code()
    printer.print_pause()
    printer.print_sections_operations()
    printer.print_pause()
    ship1.reset_operations()
    ship1.unload_containers()
    printer.print_container_code()
    print(ship1.is_balanced(1.05,1.1))
    printer.print_pause()
    printer.print_sections_operations()
    printer.print_end()

main()