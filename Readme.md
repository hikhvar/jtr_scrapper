# JTR Webscrapper

This project is a learning project for me. I want to bring the following tools together:
 - [Scrapy](http://scrapy.org/)
 - [Docker](https://www.docker.com/)
 - [ElasticSearch/Kibana](https://www.elastic.co/)

The web scrapper written with the help of scrapy, scrapps the website turniere.jugger.org which contains rankings
of almost every jugger tournament in germany. The scrapped data is written to ElasticSearch and visualized with Kibana.

## How to run


To run the ElasticSearch/Kibana you need a current version of docker and [docker-compose](https://docs.docker.com/compose/). Please have a look at the docker-compose documentation how to set this up.

First of all you need to checkout this git repository. Run
```
    git clone https://github.com/hikhvar/jtr_scrapper.git
```

Then change into the cloned directory and start the ElasticSearch/Kibana containers:
```
    cd jtr_scrapper
    docker-compose up -d
```
This will bring up one ElasticSearch-Container and one Kibana-Container. The default ports 9200 and 5601 are bound to your local machine. Thus you can reach the ElasticSearch API via http://localhost:9200 and the Kibana Webinterface via http://localhost:5601.
To run the scrapper and add data to your ElasticSearch node run:
```
    docker build -t scrapper .
    docker run --link jtrscrapper_elasticsearch_1:elasticsearch scrapper
```