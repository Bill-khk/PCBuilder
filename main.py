import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
import xlsxwriter
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium_stealth import stealth
import pandas as pd
import xlwings as xw

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

# Create XLS output file
# date = date.today()
# workbook = xlsxwriter.Workbook(f'Configuration-{date}.xlsx')
# worksheet = workbook.add_worksheet()
#
# # Add Initial parameters in the newly created XLSX file
# for comp in comp_dict:
#     col = ord(comp_dict[comp]['Init_add'][0].lower()) - 97
#     row = int(comp_dict[comp]['Init_add'][1:]) - 1
#     worksheet.write(row, col, comp_dict[comp]['Title'])
#     for parameter in comp_dict[comp]['Parameters']:
#         row += 1
#         worksheet.write(row, col, parameter)
#
# # Add Image
# image_path = 'Image/PC.png'
# cell_location = 'D9'
# worksheet.insert_image(cell_location, image_path)

# Get info
CPU_URL2 = 'https://ledenicheur.fr/c/processeurs'
CPU_URL = 'https://pcpartpicker.com/products/cpu/'


# Function to get all the raw data from a URL, return a BS4 object
def get_raw_data(URL):
    # ___________________________ Selenium options ____________________
    ua = UserAgent()
    random_user_agent = ua.random  # Get a random user-agent

    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument(f"user-agent={random_user_agent}")
    chrome_options.add_argument("--incognito")  # This prevents cookies from tracking repeated visits:
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 "
        "Safari/537.36")
    service = Service("C:/Program Files/Google/chromedriver-win64/chromedriver.exe")

    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Apply stealth mode
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    # Open the website
    driver.get(URL)

    # Disable navigator.webdriver detection
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    time.sleep(5)  # Allow time for JavaScript to load

    # Parse the page
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # Find all rows in the CPU table
    raw_data = soup.find_all("tr", class_="tr__product")

    driver.close()
    return raw_data


# Extract the information of CPUs from the webpage
def get_CPU_data():
    cpu_rows = get_raw_data(CPU_URL)
    cpu_name = [str(data)[int(str(data).find('<div class="td__nameWrapper"> <p>') + 33):str(data).find(
        '</p> <div class="td__rating"')] for data in cpu_rows]
    cpu_core = [int(str(data)[int(str(data).find('Core Count</h6>') + 15):str(data).find('Core Count</h6>') + 16]) for
                data in cpu_rows]
    cpu_perf = [float(str(data)[int(str(data).find('Performance Core Clock</h6>') + 27):str(data).find(
        'GHz</td> <td class="td__spec td__spec--3')]) for data in cpu_rows]
    cpu_price = [str(data)[int(str(data).find('<td class="td__price">') + 23):str(data).find(
        '<button class="td__add button button--small')] for data in cpu_rows]
    return [cpu_name, cpu_core, cpu_perf, cpu_price]


# Get the min configuration from the file
# TODO Change get_min_para() to avoid having to open the Book for all min component
def get_min_para(comp):
    # link component name with dict element
    comp_name = ''
    for element in comp_dict:
        if comp_dict[element]['Title'] == comp:
            comp_name = element

    print(comp_name)
    if comp_name != '':
        wb = xw.Book("Files/min_conf.xlsx")
        ws = wb.sheets['Overview']
        para = [value for value in comp_dict['cpu_tab']['Parameters']]
        para = para[:len(para) - 1]  # Remove link

        # get the coordinate of parameter
        x = chr(ord(comp_dict[comp_name]['Init_add'][:1]) + 1)
        y = str(int(comp_dict[comp_name]['Init_add'][1:]) + 1)
        para_value = []
        for value in para:
            para_value.append(ws.range(x + y).value)
            y = str(int(y) + 1)

        min_para = [(name, value) for name, value in zip(para, para_value)]
        wb.close()
        return min_para
    else:
        print('Cant find component name')
        return None


min_para_CPU = get_min_para('Processor')
print(min_para_CPU)
min_para_GPU = get_min_para('Graphic card')
print(min_para_GPU)


# Filter the cpu_info with min configuration
# TODO

# cpu_info = get_CPU_data()
#workbook.close()
