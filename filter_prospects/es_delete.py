from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

es = Elasticsearch()


def bulk_delete_index(data, via):
    print("delete indexing is started via", via)
    try:
        actions = [
            {
             "_op_type": "delete",
             "_index": "prospect_properties",
             "_type": "doc",
             "_id": obj.id,

             }
            for obj in data
        ]
        b = bulk(es, actions, request_timeout=300000)
        print("indexing complete")
        return True

    except Exception as e:
        print(e)
        return False




