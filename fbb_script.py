from nba_py.player import *
import urllib2
from bs4 import BeautifulSoup
from re import sub
from decimal import Decimal

player_splits = {}
player_prices = {}

def calculate_score(split):
	return split['PTS'] + 1.2*split['REB'] + 1.5*split['AST'] + 2*split['BLK'] + 2*split['STL'] - split['TOV']

def update_player_price(url):
    page = urllib2.urlopen(url)
    text = page.read()
    soup = BeautifulSoup(text, "lxml")
    data = str(soup.find('pre')).split('\n')[1:-1]
    for line in data:
        try:
            line = line.split(';')
            player_prices[line[3]] = Decimal(sub(r'[^\d.]', '', line[6]))
        except:
            continue

def main():
    all_players = PlayerList().info()
    for index, row in all_players.iterrows():
    	player_id = row['PERSON_ID']
    	split = PlayerGeneralSplits(player_id).overall()
    	split['POS'] = PlayerSummary(player_id).info()['POSITION']
    	split['FANTASY_SCORE'] = calculate_score(split)
    	player_splits[str(row['DISPLAY_LAST_COMMA_FIRST'])] = split
        #only grabbing first few players bc this takes FOREVER
     	if index >= 10:
     		break

    update_player_price("http://rotoguru1.com/cgi-bin/hyday.pl?game=fd&mon=4&day=12&year=2016&scsv=1")
    update_player_price("http://rotoguru1.com/cgi-bin/hyday.pl?game=fd&mon=4&day=13&year=2016&scsv=1")

    for player in player_splits:
        try:
            print player + " - "
            print split
            print player_prices[player]
        except:
            continue

if __name__ == "__main__":
    main()