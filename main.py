import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException
import requests
import xlsxwriter
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium_stealth import stealth
import pandas as pd
import xlwings as xw
from computer import Computer

comp_dict = {
    'cpu_tab': {
        'Title': 'Processor',
        'Init_add': 'A5',
        'Parameters': ['name', 'socket', 'core', 'clock_speed', 'boost_speed', 'thread', 'price', 'link'],
        'value': []
    },
    'mb_tab': {
        'Title': 'Motherboard',
        'Init_add': 'A15',
        'Parameters': ['name', 'socket', 'maxMemory', 'slotMemory', 'DDRtype', 'PCIe', 'USB2', 'USB3',
                       'Price', 'Link'],
        'value': []
    },
    'gpu_tab': {
        'Title': 'Graphic card',
        'Init_add': 'A28',
        'Parameters': ['name', 'memory', 'memoryType', 'clock_speed', 'interface', 'cooling', 'price', 'link'],
        'value': []
    },
    'ram_tab': {
        'Title': 'RAM',
        'Init_add': 'G1',
        'Parameters': ['name', 'DDRtype', 'speed', 'module_nb', 'price', 'link'],
        'value': []
    },
    'memory_tab': {
        'Title': 'Memory',
        'Init_add': 'L1',
        'Parameters': ['name', 'capacity', 'type', 'NVME', 'price', 'link'],
        'value': []
    },
    'power_tab': {
        'Title': 'Power supply',
        'Init_add': 'P1',
        'Parameters': ['name', 'type', 'wattage', 'length', 'price', 'link'],
        'value': []
    },
    'case_tab': {
        'Title': 'Case',
        'Init_add': 'T1',
        'Parameters': ['name', 'dimensions', 'price', 'link'],
        'value': []
    },
    'component': {
        'Title': 'Component',
        'Init_add': 'U8',
        'Parameters': ['Processor', 'Motherboard', 'Graphic card', 'RAM', 'Memory', 'Power supply', 'Case'],
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
def get_raw_data(URL, computer_obj):
    print('-----Getting online data')
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

    print('-----Filtering')
    # Filter website results with XLS configuration
    filter_btn = driver.find_element(By.XPATH,
                                     '//*[@id="products"]/div[4]/div[1]/div[2]/section/div/div[1]/div/div[1]/a[1]')
    filter_btn.click()
    for selector, conf in [("C", "core"), ("th", "thread"), ("A", "clock_speed")]:
        clickable = False
        div_filter = "#filter_slide_"
        left_filter = ".obj-filter-slide-left"
        while not clickable:
            try:
                web_conf_clickable = driver.find_element(By.CSS_SELECTOR, f'{div_filter}{selector} {left_filter} a')
                web_conf_clickable.click()
                clickable = True
            except ElementClickInterceptedException:
                print('Scrolling')
                driver.execute_script("document.querySelector('.offCanvas__content').scrollBy(0, 500);")
        web_conf_input = driver.find_element(By.CSS_SELECTOR, f'{div_filter}{selector} {left_filter} input')
        web_conf_input.send_keys(getattr(computer_obj.cpu, conf))  # To render dynamic

    web_hide_filter = driver.find_element(By.XPATH,
                                          '//*[@id="products"]/div[4]/div[1]/div[2]/section/div/div[1]/div/div[2]/header/nav/div/div/a')
    web_hide_filter.click()
    driver.get(driver.current_url)  # Getting filtered URL
    # Parse the page
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # Find all rows in the CPU table
    raw_data = soup.find_all("tr", class_="tr__product")

    #driver.close()
    return raw_data


# Extract the information of CPUs from the webpage
# TODO add socket, Boost speed, thread and link
def get_CPU_data(computer_obj):
    print('----------Getting online data for CPU----------')
    cpu_rows = get_raw_data(CPU_URL, computer_obj)
    cpu_name = [str(data)[int(str(data).find('<div class="td__nameWrapper"> <p>') + 33):str(data).find(
        '</p> <div class="td__rating"')] for data in cpu_rows]
    # cpu_core = [int(str(data)[int(str(data).find('Core Count</h6>') + 15):str(data).find('Core Count</h6>') + 16]) for
    #             data in cpu_rows]

    cpu_core = [int(str(data)[int(str(data).find('Core Count</h6>') + 15):str(data).find(
        '</td> <td class="td__spec td__spec--2">')]) for
                data in cpu_rows]

    cpu_perf = [float(str(data)[int(str(data).find('Performance Core Clock</h6>') + 27):str(data).find(
        'GHz</td> <td class="td__spec td__spec--3')]) for data in cpu_rows]
    cpu_price = [str(data)[int(str(data).find('<td class="td__price">') + 23):str(data).find(
        '<button class="td__add button button--small')] for data in cpu_rows]
    return [cpu_name, cpu_core, cpu_perf, cpu_price]


# TODO
def get_GPU_data(computer_obj):
    pass


# Get the min configuration from the file
def get_min_xls_conf():  #
    print('----------Retrieving minimum configuration from XLS...----------')
    min_conf = Computer()  # Create a computer object to store the para

    # Open the XLS file only once
    wb = xw.Book("Files/min_conf.xlsx")
    ws = wb.sheets['Overview']

    for pc_comp in vars(min_conf):  # Filling all component with the Computer object
        try:
            # Get the component title
            comp = getattr(min_conf, pc_comp).title
            # Link with the component name in dict element
            comp_name = ''
            for element in comp_dict:
                if comp_dict[element]['Title'] == comp:
                    comp_name = element
            # print(comp_name)  # Element got in the dict element
            # If comp_name is still empty, could find the match between computer component and dict element
            if comp_name != '':
                # Get the list of component's parameters as per the dict element
                para = [value for value in comp_dict[comp_name]['Parameters']]
                para = para[:len(para) - 1]  # Remove link

                # get the coordinate of parameter
                x = chr(ord(comp_dict[comp_name]['Init_add'][:1]) + 1)
                y = str(int(comp_dict[comp_name]['Init_add'][1:]) + 1)

                # Store the values retrieved
                para_value = []
                for value in para:
                    para_value.append(ws.range(x + y).value)
                    y = str(int(y) + 1)
                # Associating the name of the parameters with its vales
                min_para = [(name, value) for name, value in zip(para, para_value)]
                # print(min_para) # To use to see data retrieved from XLS before being put in the min_conf object

                # Put the min_para in min_conf
                for attr in dir(getattr(min_conf, pc_comp)):
                    if not attr.startswith("__") and attr not in ["title", "price", "link"] and type(attr) != bool:
                        for key, value in min_para:
                            if key == attr:
                                setattr(getattr(min_conf, pc_comp), attr, value)


            else:
                print(f'Cant find {comp} in dict element')
                return None

        except AttributeError:
            print(f'{pc_comp} is not a component')
    print('------------------------------')
    print(f'Min conf retrieved from XLS :\n{min_conf}')
    wb.close()
    return min_conf


# Create a computer object and put XLS info
min_conf = get_min_xls_conf()
# Use the created computer to filter online info
cpu_info = get_CPU_data(min_conf)
print(f'Retrieved data from URL :\n{cpu_info}')

#workbook.close()
