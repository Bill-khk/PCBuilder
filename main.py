from datetime import date
import xlsxwriter

comp_dict = {
    'cpu_tab': {
        'Title': 'Processor',
        'Init_add': 'A5',
        'Parameters': ['Name', 'Socket', 'Core', 'Clock', 'Boost', 'Thread', 'Price', 'Link'],
        'value': []
    },
    'mb_tab': {
        'Title': 'Motherboard',
        'Init_add': 'A15',
        'Parameters': ['Name', 'Socket', 'Max Memory', 'Memory Slot', 'Memory type', 'PCIe', 'USB2.0', 'USB  3.2',
                       'Price', 'Link'],
        'value': []
    },
    'gpu_tab': {
        'Title': 'Graphic card',
        'Init_add': 'A28',
        'Parameters': ['Name', 'Memory', 'Memory Type', 'Core clock', 'Interface', 'Cooling', 'Price', 'Link'],
        'value': []
    },
    'ram_tab': {
        'Title': 'RAM',
        'Init_add': 'G1',
        'Parameters': ['Name', 'Type', 'Speed', 'Module', 'Price', 'Link'],
        'value': []
    },
    'memory_tab': {
        'Title': 'Memory',
        'Init_add': 'L1',
        'Parameters': ['Name', 'Capacity', 'Type', 'NVME', 'Price', 'Link'],
        'value': []
    },
    'power_tab': {
        'Title': 'Power Supply',
        'Init_add': 'P1',
        'Parameters': ['Name', 'Type', 'Wattage', 'Length', 'Price', 'Link'],
        'value': []
    },
    'case_tab': {
        'Title': 'Case',
        'Init_add': 'T1',
        'Parameters': ['Name', 'Dimensions', 'Price', 'Link'],
        'value': []
    },
    'component': {
        'Title': 'Component',
        'Init_add': 'U8',
        'Parameters': ['Processor', 'Motherboard', 'Graphic card', 'RAM', 'Memory', 'Power Supply', 'Case'],
        'value': []
    }}

date = date.today()
workbook = xlsxwriter.Workbook(f'Configuration-{date}.xlsx')
worksheet = workbook.add_worksheet()

# Add Initial parameters
for comp in comp_dict:
    col = ord(comp_dict[comp]['Init_add'][0].lower()) - 97
    row = int(comp_dict[comp]['Init_add'][1:]) - 1
    worksheet.write(row, col, comp_dict[comp]['Title'])
    for parameter in comp_dict[comp]['Parameters']:
        row += 1
        worksheet.write(row, col, parameter)
        # print(f'{col}{row}:{parameter}')

# Add Image
image_path = 'Image/PC.png'
cell_location = 'D9'
worksheet.insert_image(cell_location, image_path)

# Get info















workbook.close()