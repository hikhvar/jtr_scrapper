# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import elasticsearchPipeline as esp

class JtrTeamRankingItem(esp.ElasticSearchBaseItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    team_name = scrapy.Field(fields={'raw': elasticsearch_dsl.String(index='not_analyzed')})
    ranking = scrapy.Field(fields={'raw': elasticsearch_dsl.String(index='not_analyzed')})
    crawl_date = scrapy.Field(fields={'raw': elasticsearch_dsl.String(index='not_analyzed')})
    hometown = scrapy.Field(fields={'raw': elasticsearch_dsl.String(index='not_analyzed')})
    points = scrapy.Field(fields={'raw': elasticsearch_dsl.String(index='not_analyzed')})
    number_of_tournaments = scrapy.Field(fields={'raw': elasticsearch_dsl.String(index='not_analyzed')})

class JtrTournamentPartition(esp.ElasticSearchBaseItem):
    id = scrapy.Field()
    team_name = scrapy.Field(fields={'raw': elasticsearch_dsl.String(index='not_analyzed')})
    tournament_name = scrapy.Field(fields={'raw': elasticsearch_dsl.String(index='not_analyzed')})
    tournament_town = scrapy.Field(fields={'raw': elasticsearch_dsl.String(index='not_analyzed')})
    ranking = scrapy.Field(fields={'raw': elasticsearch_dsl.String(index='not_analyzed')})
    tournament_date = scrapy.Field(fields={'raw': elasticsearch_dsl.String(index='not_analyzed')})
    crawl_date = scrapy.Field(fields={'raw': elasticsearch_dsl.String(index='not_analyzed')})

class JtrTournamentItem(scrapy.Item):
    id = scrapy.Field(type="string")
    tournament_name = scrapy.Field()
    tournament_date = scrapy.Field()
    participants = scrapy.Field()


