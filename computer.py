class Computer:

    def __init__(self):
        self.cpu = CPU()
        self.gpu = GPU()
        self.ram = RAM()
        self.storage = Memory()
        self.power = Power()
        self.case = Case()
        self.motherboard = Motherboard()
        self.check = True
        self.price = int

    def __str__(self):
        components = []
        for component_name in dir(self):
            if not component_name.startswith("__"):  # Ignore built-in attributes
                component = getattr(self, component_name)
                if isinstance(component, (CPU, GPU, Motherboard, Power, RAM, Memory)):  # Check if it's a known component
                    component_details = f"{component_name}:"
                    for attr_name in dir(component):
                        if not attr_name.startswith("__") and not callable(getattr(component, attr_name)):
                            attr_value = getattr(component, attr_name)
                            component_details += f"{attr_name}: {attr_value}, "
                    components.append(component_details)
        return "\n".join(components)

    def check_comp(self):
        if self.cpu.socket != self.motherboard.socket:
            self.check = False
            print('CP and Motherboard sockets is not compatible')
        elif self.motherboard.DDRtype != self.ram.DDRtype:
            self.check = False
            print('RAM and Motherboard sockets is not compatible')
        else:
            self.check = True
            print('Compatibility OK')

    def total_price(self):
        self.price = sum(getattr(self, component).price for component in self.__dict__)

class CPU:
    def __init__(self):
        self.title = 'Processor'
        self.init_add = 'A5'
        self.name = ''
        self.socket = ''
        self.core = 1
        self.clock_speed = 1
        self.boost_speed = 1
        self.thread = 1
        self.price = 0
        self.link = ''


class GPU:
    def __init__(self):
        self.title = 'Graphic card'
        self.init_add = 'A28'
        self.name = ''
        self.memory = 1
        self.memoryType = 1
        self.clock_speed = 1
        self.interface = ''
        self.cooling = 0
        self.price = 0
        self.link = ''


class RAM:
    def __init__(self):
        self.title = 'RAM'
        self.init_add = 'G1'
        self.name = ''
        self.DDRtype = 1
        self.speed = 1
        self.module_nb = 1
        self.module_size = 1
        self.price = 0
        self.link = ''


class Memory:
    def __init__(self):
        self.title = 'Memory'
        self.init_add = 'L1'
        self.name = str
        self.capacity = int
        self.type = str
        self.NVME = bool
        self.price = int
        self.link = str


class Power:
    def __init__(self):
        self.title = 'Power supply'
        self.init_add = 'P1'
        self.name = str
        self.type = str
        self.wattage = int
        self.length = int
        self.price = int
        self.link = str


class Case:
    def __init__(self):
        self.title = 'Case'
        self.init_add = 'T1'
        self.name = str
        self.dimension = {int, int, int}  # l x w x h
        self.price = int
        self.link = str


class Motherboard:
    def __init__(self):
        self.title = 'Motherboard'
        self.init_add = 'A15'
        self.name = str
        self.socket = str
        self.core = int
        self.maxMemory = int
        self.slotMemory = int
        self.DDRtype = int
        self.PCIe = int
        self.USB2 = int
        self.USB3 = int
        self.price = int
        self.link = str

