import os
import threading
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
        self.logger = {}

    @time_track
    def write_in_exel(self):
        workbook = xlsxwriter.Workbook('Itog PBI Treads.xlsx')
        worksheet = workbook.add_worksheet()
        i = 0
        for key, tag in self.logger.items():
            worksheet.write(i, 0, key)
            worksheet.write(i, 1, tag[2])
            worksheet.write(i, 2, tag[3])
            i += 1
        workbook.close()

    def parser(self, option, url, key):
        driver = webdriver.Chrome("C:\\Users\\User\\PycharmProjects\\ChromeAPI\\chromedriver.exe",
                                  options=option)
        driver.get(url)
        self.logger[key].append(
            driver.find_element_by_css_selector('meta[itemprop=image]').get_attribute('content'))
        driver.close()

    @time_track
    def urlerer(self):
        option = webdriver.ChromeOptions()
        prefs = {'profile.default_content_setting_values': {'images': 2, 'javascript': 2}}
        option.add_experimental_option('prefs', prefs)

        thread_list = []

        dict_list = [(k, v) for k, v in self.logger.items()]

        threads = 2
        c = 0 if (len(self.logger) % threads) == 0 else (threads - len(self.logger) % threads)
        print(len(self.logger) % threads)
        print(c)
        for i in range(c):
            dict_list.append(('Москва', ['https://www.google.com/maps/search/Москва', ]))

        pprint(dict_list)

        print('dlina logger', len(self.logger))
        print('dlina dict_list', len(dict_list))
        n = 0
        a = int(len(dict_list)/threads)
        print('длина цикла', a)
        for i in range(a):
            for t in dict_list[n:(n+threads)]:
                x = threading.Thread(target=self.parser, args=(option, t[1][0], t[0]))
                print('////', t[0], t[1][0])
                thread_list.append(x)
                x.start()
            for x in thread_list:
                x.join()
            n += threads

        for key, url in self.logger.items():
            a = url[1].split('?center=')[1].split('&zoom=')[0].split('%2C')
            url.extend(a)

    @time_track
    def file_opener(self):
        path = os.path.normpath(r"C:\Users\User\PycharmProjects\ChromeAPI")
        if os.path.exists(path + '\\' + 'Itog PBI Treads.xlsx'):
            os.remove(path + '\\' + 'Itog PBI Treads.xlsx')
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
                        url_created = 'https://www.google.com/maps/search/' + line_split[4][7:]
                        self.logger[line_split[4]] = [url_created, ]

    @time_track
    def run(self):
        self.file_opener()
        self.urlerer()
        self.write_in_exel()
        # for key, data in self.logger.items():
        #     print(key, ': ', data)

locatorHC = Locator()
locatorHC.run()

