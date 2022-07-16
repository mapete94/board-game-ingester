import requests
from bs4 import BeautifulSoup
import xmltodict, json
import xml.etree.ElementTree as ET

bgg = "https://boardgamegeek.com/browse/boardgame/page/1"
html = requests.get(bgg).text
soup = BeautifulSoup(html, 'html.parser')

attrs = {
    'class': 'primary'
}
for link in soup.find_all('a', attrs=attrs):
    print(link.get('href'))


bgg_xml = "https://boardgamegeek.com/xmlapi/boardgame/174430,161936?stats=1"    
xml = requests.get(bgg_xml).text

root = ET.fromstring(xml)
for boardgame in root.findall('boardgame'):
    primary_name = ""    
    mechanics = []
    categories = []
    player_count_recs = []
    for mechanic in boardgame.iter('boardgamemechanic'):
        mechanics.append(mechanic.text)

    for category in boardgame.iter('boardgamecategory'):
        categories.append(category.text)

    for name in boardgame.findall("./name[@primary='true']"):
        primary_name=name.text      

    for poll in boardgame.findall("./poll[@name='suggested_numplayers']"):
        for result in poll.iter('results'):
            player_count_rec={}
            player_count_rec['player_count']=result.attrib['numplayers']
            for answer in result.iter('result'):
                player_count_rec[answer.attrib['value']]=answer.attrib['numvotes']
            player_count_recs.append(player_count_rec)            

    bg = {
    "name": primary_name,
    "min_players": boardgame.find('minplayers').text,
    "max_players": boardgame.find('maxplayers').text,
    "playtime": boardgame.find('playingtime').text,
    "min_playtime": boardgame.find('minplaytime').text,
    "max_playtime": boardgame.find('maxplaytime').text,
    "mechanics": mechanics,
    "categories": categories,
    "average_rating": boardgame.find('statistics').find('ratings').find('average').text,
    "geek_rating": boardgame.find('statistics').find('ratings').find('bayesaverage').text,
    "users_rated": boardgame.find('statistics').find('ratings').find('usersrated').text,
    "player_count_poll": player_count_recs
    }
    print(bg)







