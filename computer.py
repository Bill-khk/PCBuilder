class Computer:

    def __init__(self):
        self.cpu = CPU()
        self.gpu = GPU()
        self.ram = RAM()
        self.storage = Storage()
        self.power = Power()
        self.case = Case()
        self.motherboard = Motherboard()
        self.check = True
        self.price = int

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
        self.name = ''
        self.memory = 1
        self.memoryType = 1
        self.clock_speed = 1
        self.interface = ''
        self.Cooling = 0
        self.price = 0
        self.link = ''


class RAM:
    def __init__(self):
        self.title = 'Memory'
        self.name = ''
        self.DDRtype = 1
        self.speed = 1
        self.module_nb = 1
        self.module_size = 1
        self.price = 0
        self.link = ''


class Storage:
    def __init__(self):
        self.title = 'Storage'
        self.name = str
        self.capacity = int
        self.type = str
        self.NVME = bool
        self.price = int
        self.link = str


class Power:
    def __init__(self):
        self.title = 'Power supply'
        self.name = str
        self.type = str
        self.wattage = int
        self.length = int
        self.price = int
        self.link = str


class Case:
    def __init__(self):
        self.title = 'Case'
        self.name = str
        self.dimension = {int, int, int}  # l x w x h
        self.price = int
        self.link = str


class Motherboard:
    def __init__(self):
        self.title = 'Motherboard'
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

