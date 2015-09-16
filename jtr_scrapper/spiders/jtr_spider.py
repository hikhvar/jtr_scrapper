__author__ = 'christoph'

import scrapy
from jtr_scrapper.items import JtrTeamRankingItem, JtrTournamentItem, JtrTournamentPartition
import datetime


class Jtr_Spider(scrapy.Spider):
    name = "jtrspider"
    allowed_domains = ["turniere.jugger.org"]
    start_urls = [ "http://turniere.jugger.org/rank.team.php" ]

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
                ranking_item['team_name'] = team_name
                if len(data) == 4:
                    ranking, city, tournaments, points = data
                else:
                    city, tournaments, points = data
                ranking_item['ranking'] = ranking
                ranking_item['hometown'] = city
                ranking_item['points'] = points
                ranking_item['number_of_tournaments'] = tournaments
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
                    date, town, ranking, zf, tw, points = data
                    item = JtrTournamentPartition()
                    item['tournament_date'] = date
                    item['date'] = datetime.datetime.now()
                    item['ranking'] = ranking.split("/")[0].strip()
                    item['team_name'] = team
                    item['tournament_town'] = town
                    item['tournament_name'] = tournament_name
                    yield item
                    #yield scrapy.Request(response.urljoin(tournament_link), callback=self.find_tournament_results)

    def find_tournament_results(self, response):
        results_link = response.xpath('//a[@title="Ergebnisse"]/@href').extract_first()
        yield scrapy.Request(response.urljoin(results_link), callback=self.parse_tournament_results)

    def parse_tournament_results(self, response):
        pass

