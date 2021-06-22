import pandas as pd
import requests
from bs4 import BeautifulSoup
columns = ['Name', 'Age', 'Position', 'Club', 'Nationality']
data = pd.DataFrame(columns = columns)
base_URL = 'https://sofifa.com/players?offset='
for offset in range(0,300):
    URL = base_URL + str(offset * 60)
    page_text = requests.get(URL).text
    soup = BeautifulSoup(page_text, features = 'html.parser')
    table_body = soup.find('tbody')
    for row in table_body:
        td = row.findAll('td')
        name = td[1].findAll('a')[0].text
        age = td[2].text
        position = td[1].findAll('a')[1].text
        club  = td[5].find('a').text
        nationality = td[1].find('img').get('title')

        player_data = pd.DataFrame([[name, age, position, club, nationality]])
        player_data.columns = columns
        data = data.append(player_data, ignore_index = True)

data = data.drop_duplicates()

data.to_csv('players_data.csv')