import requests
import json
import unittest
from bs4 import BeautifulSoup
import sqlite3
import unittest
import os


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def get_gdp(dict_return, cur, conn):

    for country in dict_return.keys():

        base_url = f"https://api.waqi.info/feed/{country}/?token=8a23bbffcf70881ba9734d4547bf4010552222ad"

        resp = requests.get(base_url)

        location_info = json.loads(resp.text)

        if (location_info['status'] == 'ok'):
            # get api
            air_quality_index = location_info['data']['aqi']

            if air_quality_index == "-":
                if "pm25" not in location_info['data']['iaqi']:
                    continue
                else:
                    air_quality_index = location_info['data']['iaqi']["pm25"]["v"]


            # get pm25
            # if "o3" not in location_info['data']['iaqi']:
            #     continue

            # pm_25_value = location_info['data']['iaqi']["o3"]["v"]

            # make country name lower case 

            # insert data into the Tracks table

            location_name = country.lower()
            location_name_capital = location_name.title()
            cur.execute('INSERT INTO AirQualityTable (Country_ID, AirQualityIndex) VALUES (?, ?)',
                (dict_return[location_name_capital], air_quality_index))

                # commit the changes
    
        conn.commit()


# def get_data(cur, conn):
# # https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key}
#     # https://worldpopulationreview.com/country-rankings/death-rate-by-country

#     dict_country_id = {}

#     url = "https://www.theglobaleconomy.com/rankings/Death_rate/"
#     r = requests.get(url)
#     soup = BeautifulSoup(r.text, 'html.parser')

#     tag = soup.find('table', class_='sortable')

#     tag1 = tag.find('tbody')

#     tag2 = tag1.find_all('tr')
    
#     count = 1
#     for tds in tag2:
#         tag3 = tds.find_all('td')

#         # index into first td and get country name
#         country_name = (tag3[0].text).strip()
#         country_name_lower = country_name.lower()
#         dict_country_id[country_name_lower] = count

#         cur.execute('INSERT INTO CountryIDTable (Country_ID, Country) VALUES (?, ?)',
#             (count, country_name_lower))

#         # index into second td and get country name
#         mortality_rate = (tag3[1].text).strip()

#         cur.execute('INSERT INTO MortalityRateTable (Country_ID, MortalityRate) VALUES (?, ?)',
#             (count, mortality_rate))
#         count = count + 1
    
#     # dict_country_id["united states"] = count
#     # count = count + 1
#     # dict_country_id["united kingdom"] = count
#     # count = count + 1
#     # dict_country_id["united arab emirates"] = count

#     conn.commit()

#     return dict_country_id


# def join_data(cur, conn):

#     cur.execute("SELECT AirQualityTable.AirQualityIndex, MortalityRateTable.MortalityRate FROM AirQualityTable JOIN MortalityRateTable ON AirQualityTable.Country = MortalityRateTable.Country")

#     count = 0
#     print('Join Data')
#     for row in cur:
#         print(row)


def get_data(cur, conn):
# https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key}
    # https://worldpopulationreview.com/country-rankings/death-rate-by-country

    dict_country_id = {}

    url = "https://statisticstimes.com/demographics/countries-by-death-rate.php"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    tag = soup.find('table', id='table_id1')

    tag1 = tag.find('tbody')

    tag2 = tag1.find_all('tr')
    
    count = 1
    for tds in tag2:
        tag3 = tds.find_all('td')

        # index into first td and get country name
        country_name = (tag3[0].text).strip()
        if (country_name == "United States of America"):
            country_name = "United States"
        if (country_name == "Russian Federation"):
            country_name = "Russia"
        if (country_name == "Iran (Islamic Republic of)"):
            country_name = "Iran"
        if (country_name == "Bolivia (Plurinational State of)"):
            country_name = "Bolivia"
        if (country_name == "Democratic Republic of the Congo"):
            country_name = "dr congo"
        if (country_name == "Viet Nam"):
            country_name = "vietnam"
        if (country_name == "Republic of Korea"):
            country_name = "South Korea"
        if (country_name == "China, Taiwan Province of China"):
            country_name = "taiwan"
        


        country_name_lower = country_name.lower()
        country_name_lower_capital = country_name_lower.title()
        dict_country_id[country_name_lower_capital] = count

        continent_name = (tag3[6].text).strip()


        cur.execute('INSERT INTO CountryIDTable (Country_ID, Country, Continent) VALUES (?, ?, ?)',
            (count, country_name_lower, continent_name))

        # index into second td and get country name
        mortality_rate = (tag3[4].text).strip()

        cur.execute('INSERT INTO MortalityRateTable (Country_ID, MortalityRate) VALUES (?, ?)',
            (count, mortality_rate))
        count = count + 1
    
    # dict_country_id["united states"] = count
    # count = count + 1
    # dict_country_id["united kingdom"] = count
    # count = count + 1
    # dict_country_id["united arab emirates"] = count

    conn.commit()

    return dict_country_id



def main():
    location_list = ["Afghanistan", "Albania", "Algeria", "Angola", "ant.& barb.", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia", "Botswana", "Brazil", "Brunei", "Bulgaria", "burkina faso", "Burma", "Burundi", "c.a. Republic", "Cambodia", "Cameroon", "Canada", "cape verde", "Chad", "Chile", "China", "Colombia", "Comoros", "costa rica", "Croatia", "Cyprus", "Czechia", "Denmark", "Djibouti", "domin. Rep.", "dr congo", "Ecuador", "Egypt", "el salvador", "eq. Guinea", "Eritrea", "estonia", "Ethiopia", "euro area", "faroe isl.", "Fiji", "Finland", "France", "french guiana", "G.-bissau", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Gibraltar", "Greece", "Grenada", "Gibraltar", "Guatemala", "Guinea", "Guyana", "Haiti", "Honduras", "hong kong", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "ivory coast", "Jamaica", "Japan", "Jersey", "Jordan", "Kazakhstan", "Kenya", "Kosovo", "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Macao", "Macedonia", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Martinique", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Mongolia", "Montenegro", "Myanmar", "Morocco", "Mozambique", "n. Caledonia", "Namibia", "Nepal", "Netherlands", "new zealand", "Nicaragua", "Niger", "Nigeria", "north korea", "north macedonia", "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "papua n.g.", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "puerto rico", "Qatar", "r. of congo", "Romania", "Russia", "Rwanda", "s.t.&principe", "saint lucia", "Samoa", "san marino", "saudi arabia", "Senegal", "Serbia", "Seychelles", "sierra leone", "singapore", "Slovakia", "Slovenia", "solomon isl.", "Somalia", "south africa", "south korea", "spain", "sri lanka", "st. vincent & …", "Sudan", "Suriname", "Swaziland", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Togo", "Tonga", "Tunisia", "Turkey", "Turkmenistan", "Uganda", "Ukraine", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican", "Venezuela", "Vietnam", "Yemen", "Zambia", "zimbabwe"]
    cur, conn = setUpDatabase('air_quality_vs_mortality_rate.db')
    
    # creating database 2 ____________________________________________________________________________
    # delete the table if it already exists
    cur.execute('DROP TABLE IF EXISTS MortalityRateTable')
    # create the table 
    cur.execute('CREATE TABLE MortalityRateTable (Country_ID INTEGER, MortalityRate INTEGER)')

    cur.execute('DROP TABLE IF EXISTS CountryIDTable')
    # create the table 
    cur.execute('CREATE TABLE CountryIDTable (Country_ID INTEGER, Country TEXT, Continent TEXT)')

    dict_return = get_data(cur, conn)

    # creating database ____________________________________________________________________________
    # delete the table if it already exists
    cur.execute('DROP TABLE IF EXISTS AirQualityTable')
    # create the table 
    cur.execute('CREATE TABLE AirQualityTable (Country_ID INTEGER, AirQualityIndex INTEGER)')
    
    get_gdp(dict_return, cur, conn)

    # join_data(cur, conn)
    

if __name__ == "__main__":
    main()