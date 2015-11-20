import scrapy
import elasticsearch_dsl
import elasticsearch
import elasticsearch.helpers
import uuid
import json

class ElasticSearchBaseItem(scrapy.Item):

    INDEX_PARAMETER = dict(drop=False)

    @classmethod
    def get_mapping(cls):
        m = elasticsearch_dsl.Mapping(cls.__name__)
        for field_name, parameters in cls.fields.iteritems():
            if "type" in parameters:
                type = parameters["type"]
                del parameters["type"]
            else:
                type = "string"
            m.field(field_name, type, **parameters)
        return m

    @classmethod
    def get_encoder_class(cls):
        class Encoder(json.JSONEncoder):
            def default(self, obj):
                if hasattr(obj, 'isoformat'):
                    return obj.isoformat()
                else:
                    return json.JSONEncoder.default(self, obj)
        return Encoder

    def get_index_name(self):
        index_name = self.__class__.__name__.lower()
        if "name" in self.INDEX_PARAMETER:
            index_name = self.INDEX_PARAMETER["name"]
        return index_name

    def get_id(self):
        return str(uuid.uuid4())

    def get_elasticsearch_document(self):
        return dict(self)



class ExampleESItem(ElasticSearchBaseItem):
    INDEX_PARAMETER = dict(name="test", drop=False)
    date = scrapy.Field(type="date")
    raw_field = scrapy.Field(type="string", fields={'raw': elasticsearch_dsl.String(index='not_analyzed')})


class ElasticSearchPipeline(object):

    INDICES = {}

    def __init__(self, host="localhost", port="9200", flush_limit=1000):
        self.counter = 0
        self.host = host
        self.port = port
        self.flush_limit = flush_limit
        self.item_queue = []
        self.es = elasticsearch.Elasticsearch(hosts=[dict(host=host, port=port)])

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.flush()

    @classmethod
    def from_crawler(cls, crawler):
        host = crawler.settings.get('ELASTICSEARCH_HOST')
        port = crawler.settings.get('ELASTICSEARCH_PORT')
        flush_limit = crawler.settings.get('ELASTICSEARCH_FLUSH_LIMIT')
        return ElasticSearchPipeline(host, port, flush_limit)


    def write(self, item):
        self.counter+=1
        self.item_queue.append(item)
        if self.counter > self.flush_limit:
            self.flush()

    def flush(self):
        json_strings = []
        for item in self.item_queue:
            index_name = item.get_index_name()
            type_name = item.__class__.__name__
            id = item.get_id()
            document = item.get_elasticsearch_document()
            action_dict = dict(_index=index_name, _type=type_name, _id=id, **document)
            json_dump = json.dumps(action_dict, cls=item.get_encoder_class())
            json_strings.append(json.loads(json_dump))
        elasticsearch.helpers.bulk(self.es, json_strings)
        self.counter=0
        self.item_queue = []

    def process_item(self, item, spider):
        if isinstance(item, ElasticSearchBaseItem):
            class_name = item.__class__.__name__
            if class_name not in self.__class__.INDICES:
                index_name = item.get_index_name()
                mapping = item.__class__.get_mapping()
                if "drop" in item.INDEX_PARAMETER:
                    if item.INDEX_PARAMETER["drop"]:
                        self.es.indices.delete(index=index_name, ignore=[404])
                mapping.save(index_name, using = self.es)
                self.__class__.INDICES[class_name] = dict(mapping=mapping, index_name=item.get_index_name())
            self.write(item)
        return item
