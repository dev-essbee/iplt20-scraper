from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import numpy as np
from PyInquirer import prompt
import os
import signal
import sys


def error_msg():
    print('You pressed Ctrl+C!')
    exit_application()


def exit_application():
    print('Exiting the application')
    sys.exit(0)


def signal_handler(sig, frame):
    error_msg()


signal.signal(signal.SIGINT, signal_handler)


def save_data(data, columns, data_set_name, file_name):
    df = pd.DataFrame(data, columns=columns)
    file_path = './' + file_name + '-' + data_set_name + '.csv'
    df.to_csv(file_path, index=False)
    print(data_set_name + ' saved as: ' + os.path.dirname(os.path.abspath(__file__)) + '/' + data_set_name + '.csv')


def get_team_data(soup, columns):
    data = []
    for i in soup.find_all('td'):
        data.append(re.sub(r'\n[\s]*', " ", i.get_text().strip()))
    data = np.array(data).reshape(len(data) // len(columns), len(columns) + 1)
    data = np.delete(data, 0, axis=1)
    return data, columns


def get_player_data(soup, columns):
    data = []
    for i in soup.find_all('td', class_=re.compile(r'top-players*')):
        data.append(re.sub(r'\n[\s]*', " ", i.get_text().strip()))
    data = np.array(data).reshape(len(data) // len(columns), len(columns))
    return data, columns


def find_col(soup, team):
    try:
        if team:
            columns = list(filter(None, soup.find('tr', class_='standings-table__header').get_text().split('\n')))
            return get_team_data(soup, columns)
        else:
            columns = re.sub(r'\n[\s]*', '\n',
                             soup.find('tr', class_=re.compile(r'top-players__header*')).get_text()).strip().split('\n')
            return get_player_data(soup, columns)
    except AttributeError:
        return [], []


def scrap_data(years, stats):
    base = 'https://www.iplt20.com/stats/'
    base_file_name = 'Result'
    for year in years:
        for stat in stats:
            if stat == 'team-ranking':
                url = base + year
                data, columns = get_page(url, True)
                data_set_name = 'Team-Ranking-' + year
            else:
                url = base + year + '/' + stat
                data, columns = get_page(url, False)
                data_set_name = str.title(stat) + '-' + year
            if len(data) == 0:
                print(data_set_name + ' :' + 'Data not Available')
            else:
                save_data(data, columns, data_set_name, base_file_name)


def get_page(url, team):
    try:
        page = requests.get(url)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            data, columns = find_col(soup, team)
            return data, columns
        else:
            print('Website Unreachable')
            return
    except requests.exceptions.ConnectionError:
        print('Please check network connection')
        return


def get_years(soup):
    years = [year.get_text() for year in soup.find_all('a', class_=re.compile(r'sub-menu*'))]
    years[-1] = 'all-time'
    return years


def get_stats(soup):
    stats = soup.find_all('a', class_=re.compile(r'side*'))
    stats_url = [re.search(r'\d/(.*)', stat['href']).group(1) for stat in stats]
    stats_title = [re.sub(r'[\n]+', '\n', stat.get_text()).strip() for stat in stats]
    return stats_url, stats_title


def get_year_stats():
    url = 'https://www.iplt20.com/stats/2019'
    years = []
    stats_url = []
    stats_title = []
    try:
        page = requests.get(url)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            years = get_years(soup)
            stats_url, stats_title = get_stats(soup)
            stats_url.append('team-ranking')
            stats_title.append('Team Ranking')
    except requests.exceptions.ConnectionError:
        print('Please check network connection')
        return
    return years, stats_url, stats_title


def prepare_question(years, stats_title, stats_url):
    years_dic_list = [{'name': year} for year in years]
    stats_dic_list = [{'name': stats_title[i], 'value': stats_url[i]} for i in range(len(stats_title))]
    return years_dic_list, stats_dic_list


def user_input(years_q, stats_q):
    answers = {'years': '', 'stats': ''}
    try:
        while len(answers.get('years')) == 0 or len(answers.get('stats')) == 0:
            questions = [
                {
                    'type': 'checkbox',
                    'message': 'Select years',
                    'name': 'years',
                    'choices': years_q,
                }, {
                    'type': 'checkbox',
                    'message': 'Select statistics',
                    'name': 'stats',
                    'choices': stats_q,
                }
            ]
            answers = prompt(questions)
    except TypeError:
        error_msg()
    except EOFError:
        exit_application()
    return answers['years'], answers['stats']


def main():
    years, stats_url, stats_title = get_year_stats()
    years_q, stats_q = prepare_question(years, stats_title, stats_url)
    years, stats = user_input(years_q, stats_q)
    print('Collecting and saving data.')
    scrap_data(years, stats)


if __name__ == '__main__':
    try:
        main()
    except AssertionError:
        print('Interface not supported, please use terminal or command prompt.')
