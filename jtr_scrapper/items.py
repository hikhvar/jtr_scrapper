# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import elasticsearchPipeline as esp
import elasticsearch_dsl

class JtrTeamRankingItem(esp.ElasticSearchBaseItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    INDEX_PARAMETER = dict(name="global_ranking", drop=False)
    team_name = scrapy.Field(fields={'raw': elasticsearch_dsl.String(index='not_analyzed')})
    ranking = scrapy.Field(type="integer")
    crawl_date = scrapy.Field(type="date", fields={'raw': elasticsearch_dsl.String(index='not_analyzed')})
    hometown = scrapy.Field(fields={'raw': elasticsearch_dsl.String(index='not_analyzed')})
    points = scrapy.Field(type="float")
    number_of_tournaments = scrapy.Field(fields={'raw': elasticsearch_dsl.String(index='not_analyzed')})

class JtrTournamentPartition(esp.ElasticSearchBaseItem):
    INDEX_PARAMETER = dict(name="tournament_partitions", drop=True)
    team_name = scrapy.Field(stored=True, fields={'raw': elasticsearch_dsl.String(index='not_analyzed')})
    team_hometown = scrapy.Field(stored=True, fields={'raw': elasticsearch_dsl.String(index='not_analyzed')})
    team_hometown_position = scrapy.Field(stored=True, type="geo_point")
    tournament_name = scrapy.Field(stored=True, fields={'raw': elasticsearch_dsl.String(index='not_analyzed')})
    tournament_town = scrapy.Field(stored=True, fields={'raw': elasticsearch_dsl.String(index='not_analyzed')})
    tournament_town_position = scrapy.Field(stored=True, type="geo_point")
    distance = scrapy.Field(stored=True, type="float")
    ranking = scrapy.Field(type="integer", stored=True, fields={'raw': elasticsearch_dsl.String(index='not_analyzed')})
    tournament_date = scrapy.Field(type="date", fields={'raw': elasticsearch_dsl.String(index='not_analyzed')})
    crawl_date = scrapy.Field(type="date", fields={'raw': elasticsearch_dsl.String(index='not_analyzed')})

class JtrTournamentItem(scrapy.Item):
    tournament_name = scrapy.Field()
    tournament_date = scrapy.Field()
    participants = scrapy.Field()


