import unidecode
import pandas as pd
import requests
from bs4 import BeautifulSoup
columns = ['Name', 'Age', 'Position', 'Club', 'Nationality']
data = pd.DataFrame(columns = columns)
BASE_URL = 'https://sofifa.com/players?offset='

def remove_accent(accented_string):
    """
    remove accent in players' and clubs' name
    """
    unaccented_string = unidecode.unidecode(accented_string)
    return unaccented_string
def test_remove_accent():
    """
    test remove_accent()
    """
    accented_input_string = 'Málaga FC'
    desire_output = 'Malaga FC'
    assert desire_output == remove_accent(accented_input_string), "Mistake in removing accent"

if __name__ == "__main__":
    for offset in range(0,300):
        URL = BASE_URL + str(offset * 60)
        page_text = requests.get(URL).text
        soup = BeautifulSoup(page_text, features = 'html.parser')
        table_body = soup.find('tbody')
        for row in table_body:
            td = row.findAll('td')
            name = td[1].findAll('a')[0].text
            name = remove_accent(name)
            age = td[2].text
            position = td[1].findAll('a')[1].text
            club  = td[5].find('a').text
            club = remove_accent(club)
            nationality = td[1].find('img').get('title')

            player_data = pd.DataFrame([[name, age, position, club, nationality]])
            player_data.columns = columns
            data = data.append(player_data, ignore_index = True)

    data = data.drop_duplicates()
    data.to_csv('players_data.csv')
