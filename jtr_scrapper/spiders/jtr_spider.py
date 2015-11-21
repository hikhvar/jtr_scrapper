__author__ = 'christoph'

import scrapy
from jtr_scrapper.items import JtrTeamRankingItem, JtrTournamentItem, JtrTournamentPartition
import datetime
import uuid
import utils
import Geohash as geohash
import geopy
import geopy.exc
import geopy.distance as geodistance

class Jtr_Spider(scrapy.Spider):
    name = "jtrspider"
    allowed_domains = ["turniere.jugger.org"]
    start_urls = [ "http://turniere.jugger.org/rank.team.php" ]
    geo_locator = geopy.Nominatim()
    location_cache = {}

    def parse(self, response):
        title = response.xpath('//div[@class="title"]/text()').extract_first()
        if title == "Teamwertung":
            return self.parse_starting_page(response)


    def parse_starting_page(self, response):
        ranking = 0
        for sel in response.xpath('//div[@class="content"]/table/tr'):
            team_link = sel.xpath('td/a/@href').extract_first()
            if team_link is not None:
                team_name = sel.xpath('td/a/text()').extract_first()
                data = sel.xpath('td/text()').extract()
                ranking_item = JtrTeamRankingItem()
                ranking_item['team_name'] = utils.unescape(team_name)
                if len(data) == 4:
                    ranking, city, tournaments, points = data
                else:
                    city, tournaments, points = data
                ranking_item['ranking'] = int(ranking.split("/")[0].strip().strip("."))
                ranking_item['hometown'] = utils.unescape(city)
                ranking_item['points'] = float(points)
                ranking_item['number_of_tournaments'] = utils.unescape(tournaments)
                ranking_item['crawl_date'] = datetime.datetime.now()
                yield  ranking_item
                yield scrapy.Request(response.urljoin(team_link), callback=self.parse_team_site)

    def parse_team_site(self, response):
        team = response.xpath('//div[@class="title"]/text()').extract_first()
        for sel in response.xpath('//div[@class="content"]/table/tr'):
            tournament_link = sel.xpath('td/a/@href').extract_first()
            if tournament_link is not None:
                data = sel.xpath('td/text()').extract()
                tournament_name = sel.xpath('td/a/text()').extract_first()
                if len(data) == 6:
                    date, tournament_town, ranking, zf, tw, points = data
                    item = JtrTournamentPartition()
                    item['tournament_date'] = date
                    item['crawl_date'] = datetime.datetime.now()
                    item['ranking'] = int(ranking.split("/")[0].strip().strip("."))
                    home_town, team_name = team.split("-", 1)
                    item['team_name'] = utils.unescape(team_name.strip())
                    item['team_hometown'] = utils.unescape(home_town.strip())
                    item['tournament_town'] = utils.unescape(tournament_town)
                    item['tournament_name'] = utils.unescape(tournament_name)
                    home_town = self._locate(home_town)
                    tournament_town = self._locate(tournament_town)
                    item["team_hometown_position"] = self._get_geohash(home_town)
                    item["tournament_town_position"] = self._get_geohash(tournament_town)
                    item["distance"] = self._get_distance(home_town, tournament_town)
                    yield item
                    #yield scrapy.Request(response.urljoin(tournament_link), callback=self.find_tournament_results)

    def find_tournament_results(self, response):
        results_link = response.xpath('//a[@title="Ergebnisse"]/@href').extract_first()
        yield scrapy.Request(response.urljoin(results_link), callback=self.parse_tournament_results)

    def parse_tournament_results(self, response):
        pass

    def _locate(self, town_name):
        town_name = utils.unescape(town_name.strip())
        if town_name not in self.location_cache:
            try:
                self.location_cache[town_name] = self.geo_locator.geocode(town_name)
            except geopy.exc.GeocoderTimedOut:
                print "Geocoder Timeout."
                return None
        return self.location_cache[town_name]


    def _get_geohash(self, town):
        if town is not None:
            return geohash.encode(town.latitude, town.longitude)
        else:
            return None

    def _get_distance(self, town_a, town_b):
        if town_a is None or town_b is None:
            return None
        else:
            return geodistance.great_circle(town_a.point, town_b.point).kilometers
