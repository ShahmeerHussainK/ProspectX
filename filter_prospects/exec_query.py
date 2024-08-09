from elasticsearch import Elasticsearch
from urllib.parse import unquote

client = Elasticsearch()


def list_tag_count(obj, user_id):
    list_count_final = []
    tag_count_final = []
    all_lists = obj['list']
    all_tags = obj['tag']
    for list in all_lists:
        if list["user"]["id"] in user_id:
            list_count_final.append(list)
    for tag in all_tags:
        if tag["user"]["id"] in user_id:
            tag_count_final.append(tag)
    list_count = len(list_count_final)
    tag_count = len(tag_count_final)
    return list_count, tag_count


def run_els_query(data, action='all'):

    res_list = []
    search_query = data["search_query"]
    user_id = data["user_id"]
    list_included = data["list_included"]
    if list_included:
        if isinstance(list_included, str):
            list_included = list(list_included.split(","))
    tag_included = data["tag_included"]
    if tag_included:
        if isinstance(tag_included, str):
            tag_included = list(tag_included.split(","))
    list_excluded = data["list_excluded"]
    if list_excluded:
        if isinstance(list_excluded, str):
            list_excluded = list(list_excluded.split(","))
    tag_excluded = data["tag_excluded"]
    if tag_excluded:
        if isinstance(tag_excluded, str):
            tag_excluded = list(tag_excluded.split(","))
    list_count = data["list_count"]
    list_count_total = data["list_count_total"]
    tag_count = data["tag_count"]
    tag_count_total = data["tag_count_total"]
    absentee = data["absentee"]
    vacant = data["vacant"]
    skipped = data["skipped"]
    opt_out = data["opt_out"]
    radio_list_in = data["radio_list_in"]
    radio_tag_in = data["radio_tag_in"]
    body = {}

    # User must be in queryset
    must = [{
        "terms": {
            # "list.user.id": [user_id]
            "list.user.id": user_id
        }
    }]
    must_not = []

    # Search
    if search_query:
        multi_match = {
            "multi_match": {
                "query": search_query,
                "fields": ["fullname", "propertyaddress^3", "firstname", "mailingaddress"],
                "fuzziness": "AUTO"
            }
        }
        must.append(multi_match)

    validate_query = {
        "match": {
            "is_validate_complete": True
        }
    }
    must.append(validate_query)

    if list_included:
        if radio_list_in == "in":
            list_must_in = {
                "terms": {
                    "list.id": list_included
                }
            }
            must.append(list_must_in)
        elif radio_list_in == "on":
            for index in range(len(list_included)):
                list_must_on = {
                    "terms": {
                        "list.id": [list_included[index]]
                    }
                }
                must.append(list_must_on)

    if tag_included:
        if radio_tag_in == "in":
            tag_must_in = {
                "terms": {
                    "tag.id": tag_included
                }
            }
            must.append(tag_must_in)
        elif radio_tag_in == "on":
            for index in range(len(tag_included)):
                tag_must_on = {
                    "terms": {
                        "tag.id": [tag_included[index]]
                    }
                }
                must.append(tag_must_on)
    if list_excluded:
        list_must_not = {
            "terms": {
                "list.id": list_excluded
            }
        }
        must_not.append(list_must_not)
    if tag_excluded:
        tag_must_not = {
            "terms": {
                "tag.id": tag_excluded
            }
        }
        must_not.append(tag_must_not)

    if absentee:
        absentee_query = {
            "match": {
                "absentee": absentee
            }
        }
        must.append(absentee_query)
    if vacant:
        vacant_query = {
            "match": {
                "vacant": data["vacant"]
            }
        }
        must.append(vacant_query)

    if skipped:
        skipped_query = {
            "match": {
                "skipped": data["skipped"]
            }
        }
        must.append(skipped_query)
    else:
        skipped_query = {
            "match": {
                "skipped": False
            }
        }
        must.append(skipped_query)

    if 'Both' not in data["opt_out"]:
        opt_out_query = {
            "match": {
                "opt_out": data["opt_out"]
            }
        }
        must.append(opt_out_query)
    if isinstance(data["select_key"], str):
        data["select_key"] = list(data["select_key"].split(","))
        data["select_con"] = list(data["select_con"].split(","))
        data["select_val"] = list(data["select_val"].split(","))

    if data["select_key"]:
        filter = {}
        filter["bool"] = {}

        bool_must = {
            "bool": {
                "must": []
            }}
        bool_must_not = {
            "bool": {
                "must_not": []
            }}
        bool_should = {
            "bool": {
                "should": []
            }}
        for index in range(len(data["select_key"])):
            selected_key = data["select_key"][index]
            if selected_key != '-1':
                if data["select_con"][index] == 'contains':
                    cus_var = {
                        "match_phrase": {
                            data["select_key"][index]: unquote(data["select_val"][index])
                        }
                    }
                    if data["filters_condition"] == "or":
                        bool_should["bool"]["should"].append(cus_var)
                    elif data["filters_condition"] == "and":
                        bool_must["bool"]["must"].append(cus_var)
                elif data["select_con"][index] == 'not_contains':
                    cus_var = {
                        "match_phrase": {
                            data["select_key"][index]: unquote(data["select_val"][index])
                        }
                    }
                    bool_must_not["bool"]["must_not"].append(cus_var)
                elif data["select_con"][index] == 'is_empty':
                    cus_var = {
                        "exists": {
                            "field": data["select_key"][index]
                        }
                    }
                    bool_must_not["bool"]["must_not"].append(cus_var)
                elif data["select_con"][index] == 'is_not_empty':
                    cus_var = {
                        "exists": {
                            "field": data["select_key"][index]
                        }
                    }
                    bool_must["bool"]["must"].append(cus_var)

    if data["filters_condition"] == 'or':
        filter["bool"].update({"should": []})
        if bool_must["bool"]["must"]:
            filter["bool"]["should"].append(bool_must)
        if bool_must_not["bool"]["must_not"]:
            filter["bool"]["should"].append(bool_must_not)
        if bool_should["bool"]["should"]:
            filter["bool"]["should"].append(bool_should)
    elif data["filters_condition"] == 'and':
        filter["bool"].update({"must": []})
        if bool_must["bool"]["must"]:
            filter["bool"]["must"].append(bool_must)
        if bool_must_not["bool"]["must_not"]:
            filter["bool"]["must"].append(bool_must_not)
        if bool_should["bool"]["should"]:
            filter["bool"]["must"].append(bool_should)

    body['query'] = {
        "bool": {
            "must": must,
            "must_not": must_not,
            "filter": filter
        }
    }
    params = {}

    if list_count or tag_count:
        list_count_loop = """int lists_all = params["_source"]["list"].length;"""
        tag_count_loop = """int tags_all = params["_source"]["tag"].length;"""
        list_cond = """lists_all >= params["param_list_count"] && lists_all <= params["param_list_count_total"]"""
        tag_cond = """ tags_all >= params["param_tag_count"] &&  tags_all<= params["param_tag_count_total"] """
        and_var = """&&"""
        if list_count:
            cus_str = list_count_loop + """if ( """ + list_cond + """ ) { return 1; } else { return 0;}"""  # its working perfectly fine
            params.update({"param_list_count": int(list_count)})
            params.update({"param_list_count_total": int(list_count_total)})
        if tag_count:
            cus_str = tag_count_loop + """if ( """ + tag_cond + """ ) { return 1; } else { return 0;}"""  # its working perfectly fine
            params.update({"param_tag_count": int(tag_count)})
            params.update({"param_tag_count_total": int(tag_count_total)})
        if list_count and tag_count:
            cus_str = list_count_loop + tag_count_loop + """if ( """ + list_cond + and_var + tag_cond + """ ) { return 1; } else { return 0;}"""  # its working perfectly fine
            params.update({"param_list_count": int(list_count)})
            params.update({"param_list_count_total": int(list_count_total)})
            params.update({"param_tag_count": int(tag_count)})
            params.update({"param_tag_count_total": int(tag_count_total)})
        cus_func = [{
            "script_score": {
                "script": {
                    "source": cus_str,
                    "params": params
                }
            }
        }]
        final_body = {}

        final_body['query'] = {
            "function_score": body
        }

        final_body['query']['function_score'].update({
            "functions": cus_func
        })
        if action == "ids":
            final_body['size'] = 10000
            final_body['from'] = 0
            final_body['_source'] = ["id"]
        else:
            final_body['size'] = data['length']
            final_body['from'] = data['start']
            final_body['_source'] = ["id", "fullname", "propertyaddress", "mailingaddress", "list", "tag"]

        final_body["min_score"] = 0.1
        search_result = client.search(index='prospect_properties', doc_type='doc', body=final_body)
    else:
        if action == "ids":
            body['size'] = 10000
            body['from'] = 0
            body['_source'] = ["id"]
        else:
            body['size'] = data['length']
            body['from'] = data['start']
            body['_source'] = ["id", "fullname", "propertyaddress", "mailingaddress", "list", "tag"]
        search_result = client.search(index='prospect_properties', doc_type='doc', body=body)

    total = search_result['hits']['total']
    for hit in search_result['hits']['hits']:
        res_obj = hit["_source"]
        if action == "ids":
            res_list.append(res_obj["id"])
        else:
            list_count, tag_count = list_tag_count(hit["_source"], user_id)
            res_obj.update(list_count=list_count, tag_count=tag_count, sequence="abc")
            del res_obj['list']
            del res_obj['tag']
            res_list.append(res_obj)

    return res_list, total
