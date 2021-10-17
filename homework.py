import os
from os import listdir
from os.path import isfile, join
import time
import warnings
from selenium.webdriver.chrome.options import Options
import selenium.webdriver as webdriver
import PyPDF2
from conf import query


warnings.filterwarnings("ignore")

# Выбираем путь для сохранения файла и инициализируем сессию

file_path = "/Users/andreychubin/Desktop/ВШЭ/RPA.ipynb"
working_dir = os.path.dirname(os.path.realpath(file_path))
webdriver_path = os.path.join(working_dir, "chromedriver")
save_dir = "/Users/andreychubin/Desktop/ВШЭ"

options = Options()

options.add_experimental_option('prefs', {
    "download.default_directory": save_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
    })

os.environ["webdriver.chrome.driver"] = webdriver_path
driver = webdriver.Chrome(executable_path=webdriver_path, options=options)

# Заходим на сайт

query_link = "https://www.semanticscholar.org/"
driver.get(query_link)

time.sleep(2)

# Находим поле для ввода и кнопку Submit

field = driver.find_element_by_xpath('//*[@id="search-form"]/div/div/input')
submit = driver.find_element_by_xpath('//*[@id="search-form"]/div/div/button')

# Присупаем к выполнению

field.click()
field.clear()
field.send_keys(query)
submit.click()
time.sleep(2)

article = driver.find_element_by_xpath('//*[@id="main-content"]/div[1]/div[1]/div[3]/a/div')
article.click()
time.sleep(2)

# Находим статью, у которой есть ссылка для скачивания и скачиваем файл

link = driver.find_element_by_xpath('//*[@id="paper-header"]/div/div[1]/div/div/div/a')
link.click()
time.sleep(1)

# Завершаем сессию

driver.get("https://youtu.be/dQw4w9WgXcQ")

time.sleep(15)

driver.close()

# Находим файл в папке

pdf = [f for f in listdir(save_dir) if isfile(join(save_dir, f)) if "pdf" in f]

# Открываем скачанный файл и просматриваем некоторое содержимое

pdfFileObj = open(save_dir + '/' + pdf[0], 'rb')

pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

print(f"Num pages: {pdfReader.numPages}")
print(" ")

pageObj1 = pdfReader.getPage(0)

print("-----First Page-----")
print(" ")
print(pageObj1.extractText())
print(" ")

pageObj2 = pdfReader.getPage(1)

print("-----Second Page-----")
print(" ")
print(pageObj2.extractText())

# Закрываем файл

pdfFileObj.close()
