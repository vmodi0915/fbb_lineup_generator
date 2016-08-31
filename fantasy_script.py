from basketball_reference_web_scraper.readers import *
import urllib2
from bs4 import BeautifulSoup
from re import sub
from decimal import Decimal

player_stat_lines = {}
player_scores = {}
player_price = {}

def calculate_score(stat_line):
    rebounds = float(stat_line.offensive_rebounds) + float(stat_line.defensive_rebounds)
    return (float(stat_line.points) + 1.2*float(rebounds) + 1.5*float(stat_line.assists) + 2*float(stat_line.blocks) + 2*float(stat_line.steals) - float(stat_line.turnovers))/float(stat_line.games_played)

def update_player_price(url):
    try:
        page = urllib2.urlopen(url)
        text = page.read()
        soup = BeautifulSoup(text)
        data = str(soup.find('pre')).split('\n')[1:-1]
        for line in data:
            line = line.split(';')
            player_price[line[3]] = Decimal(sub(r'[^\d.]', '', line[6]))
    except:
        pass

def main():
    for stat_line in return_all_player_season_statistics(2015):
        name = stat_line.last_name + ", " + stat_line.first_name 
        player_stat_lines[name] = stat_line
        player_scores[name] = calculate_score(stat_line)

    update_player_price("http://rotoguru1.com/cgi-bin/hyday.pl?game=fd&mon=4&day=12&year=2016&scsv=1")
    update_player_price("http://rotoguru1.com/cgi-bin/hyday.pl?game=fd&mon=4&day=13&year=2016&scsv=1")
    print player_price 

    for name in sorted(player_scores, key=player_scores.get, reverse=True)[:10]:
        print name + " - " + str(player_scores[name])

if __name__ == "__main__":
    main()
