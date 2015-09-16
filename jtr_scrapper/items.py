# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JtrTeamRankingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    team_name = scrapy.Field()
    ranking = scrapy.Field()
    crawl_date = scrapy.Field()
    hometown = scrapy.Field()
    points = scrapy.Field()
    number_of_tournaments = scrapy.Field()

class JtrTournamentPartition(scrapy.Item):
    team_name = scrapy.Field()
    tournament_name = scrapy.Field()
    tournament_town = scrapy.Field()
    ranking = scrapy.Field()
    tournament_date = scrapy.Field()
    date = scrapy.Field()

class JtrTournamentItem(scrapy.Item):
    tournament_name = scrapy.Field()
    tournament_date = scrapy.Field()
    participants = scrapy.Field()


