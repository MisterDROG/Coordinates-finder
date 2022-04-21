import os
import time
import xlsxwriter
from selenium import webdriver
from pprint import pprint

def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()
        result = func(*args, **kwargs)
        ended_at = time.time()
        elapsed = round(ended_at - started_at, 4)
        print(f'Функция {func.__name__} работала {elapsed} секунд(ы)')
        return result
    return surrogate

class Locator:
    def __init__(self):
        self.logger = []

    @time_track
    def write_in_exel(self):
        workbook = xlsxwriter.Workbook('Itog PBI.xlsx')
        worksheet = workbook.add_worksheet()
        i = 0
        for tag in self.logger:
            worksheet.write(i, 0, tag[0])
            worksheet.write(i, 1, tag[2])
            worksheet.write(i, 2, tag[3])
            i += 1
        workbook.close()

    @time_track
    def urlerer(self):
        Url_With_Coordinates = []
        option = webdriver.ChromeOptions()
        prefs = {'profile.default_content_setting_values': {'images': 2, 'javascript': 2}}
        option.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome("C:\\Users\\User\\PycharmProjects\\ChromeAPI\\chromedriver.exe",
                                  options=option)
        _ = 0
        for url in self.logger:
            driver.get(url[1])
            Url_With_Coordinates.append(
                driver.find_element_by_css_selector('meta[itemprop=image]').get_attribute('content'))
            _ += 1
            print('Координат собрано:', _)
        driver.close()
        l = 0
        for url in Url_With_Coordinates:
            a = url.split('?center=')[1].split('&zoom=')[0].split('%2C')
            self.logger[l].extend(a)
            l += 1

    @time_track
    def file_opener(self):
        path = os.path.normpath(r"C:\Users\User\PycharmProjects\ChromeAPI")
        if os.path.exists(path + '\\' + 'Itog PBI.xlsx'):
            os.remove(path + '\\' + 'Itog PBI.xlsx')
        fileList = os.listdir(path)
        for file in fileList:
            if file[-3:] == 'csv':
                with open(os.path.join(path + '\\' + file), 'r', encoding='utf-8') as file:
                    i = 0
                    for line in file:
                        if i <= 0:
                            i += 1
                            continue
                        line_split = line.split(',')
                        line_split[7] = 'https://www.google.com/maps/search/' + line_split[4][7:]
                        self.logger.append([line_split[4], line_split[7]])

    @time_track
    def run(self):
        self.file_opener()
        self.urlerer()
        self.write_in_exel()


locatorHC = Locator()
locatorHC.run()

