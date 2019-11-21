from urllib.parse import quote
import csv
import os
import math
import platform

from bs4 import BeautifulSoup
from selenium import webdriver


class Parser:
    def __init__(self):
        executable = ''
        if platform.system() == 'Windows':
            print('Detected OS : Windows')
            executable = './driver/chromedriver_win.exe'
        elif platform.system() == 'Darwin':
            print('Detected OS : Mac')
            executable = './driver/chromedriver_mac'
        else:
            raise OSError('Unknown OS Type')
        if not os.path.exists(executable):
            raise FileNotFoundError('Chromedriver file should be placed at {}'.format(executable))

        self.browser = webdriver.Chrome(executable)

    def get(self, url):
        print('parsing {url} ...'.format(url=url))
        self.browser.get(url)
        html = self.browser.page_source

        soup = BeautifulSoup(html, features='lxml')
        string_result = soup.find("div", {"id": "resultStats"}).contents[0].split(' ')[2]

        temp = []
        for letter in string_result:
            if letter.isdigit():
                temp.append(int(letter))
            elif letter == ',':
                continue
            else:
                break

        result = 0
        place = len(temp) - 1
        for digit in temp:
            result += int(digit * math.pow(10, place))
            place -= 1

        return result

    def close(self):
        self.browser.close()


parser = Parser()


def parse_file(csv_path):
    result = []
    with open(csv_path) as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            query = row[0]
            url = 'https://www.google.com/search?q={query}'.format(query=quote(query))
            search_result = parser.get(url=url)
            result.append([query, search_result])
    return result


if __name__ == '__main__':
    root = os.path.realpath(os.path.dirname(__file__))

    parsed_data = []

    # Parse CSV
    input_csv_files = [file_name for file_name in os.listdir(os.path.join(root, 'input')) if file_name.endswith('.csv')]
    for csv_file_name in input_csv_files:
        csv_file_path = os.path.join(root, 'input', csv_file_name)
        result = parse_file(csv_file_path)

        with open(os.path.join(root, 'output', csv_file_name), 'w') as output_file:
            writer = csv.writer(output_file, lineterminator = '\n')
            writer.writerows(result)
            output_file.close()

    parser.close()
