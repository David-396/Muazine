import re

from base64_decrypt import decrypt_from_base64
from es_dal import ESConnector
from es_crud import CRUD

hostile ="R2Vub2NpZGUsV2FyIENyaW1lcyxBcGFydGhlaWQsTWFzc2FjcmUsTmFrYmEsRGlzcGxhY2VtZW50LEh1bWFuaXRhcmlhbiBDcmlzaXMsQmxvY2thZGUsT2NjdXBhdGlvbixSZWZ1Z2Vl cyxJQ0MsQkRT"

less_hostile ="RnJlZWRvbSBGbG90aWxsYSxSZXNpc3RhbmNlLExpYmVyYXRpb24sRnJlZSBQYWxlc3RpbmUsR2F6YSxDZWFzZWZpcmUsUHJvdGVzdCxVTlJXQQ=="

hostiles_lst = decrypt_from_base64(hostile).lower().split(',')
less_hostile_lst = decrypt_from_base64(less_hostile).lower().split(',')
# print(hostiles_lst)

ES_INDEX='json_files_metadata'

with ESConnector(host='localhost', port=9200) as es_client:
    es_crud = CRUD(es_client=es_client.get_client())

    query = {
  "query": {
      "bool":{
          "must":{
    "match": {
      "metadata.recognized_text": ' '.join(hostiles_lst)
    }
  }
}
  }}

    a = es_crud.get_by_query(index_name=ES_INDEX, query=query, size=20)
    a=es_crud.get_all_docs(index_name=ES_INDEX, size=20)
    print(a)
    print(' '.join(less_hostile_lst))
    print('############################ less hostile')

    # query = {
    #     "query": {
    #         "match": {
    #                     "metadata.recognized_text": ' '.join(less_hostile_lst)
    #                 }
    #             }
    #         }

    less_hostile_query = {
  "query": {
    "match": { "metadata.recognized_text": ' '.join(less_hostile_lst) }
  },
  "highlight": {
    "fields": {
      "metadata.recognized_text": {}
    }
  }
}

    a = es_crud.get_by_query(index_name=ES_INDEX, query=less_hostile_query, size=20)
    # a=es_crud.get_all_docs(index_name=ES_INDEX, size=20)
    # print(a)

    for doc in a:
        all_text = doc['_source']['metadata']['recognized_text'].split(' ')
        words_txt = doc['highlight']['metadata.recognized_text']
        # print(all_text)
        words_detected = []
        for word in words_txt:
            word_detect = ' '.join(re.findall(r"<em>(.*?)</em>", word))
            words_detected.append(word_detect)

        score = doc['_score']
        percent_hostile_to_text = len(words_txt)/len(all_text)
        print(words_detected, len(all_text), len(words_txt), "PERCENT:",percent_hostile_to_text, "_SCORE:", doc['_score'], "SUM_PERCENT:",score*percent_hostile_to_text)


    print('####################### hostile:')
    hostile_query = {
        "query": {
            "match": {"metadata.recognized_text": ' '.join(hostiles_lst)}
        },
        "highlight": {
            "fields": {
                "metadata.recognized_text": {}
            }
        }
    }

    a = es_crud.get_by_query(index_name=ES_INDEX, query=hostile_query, size=20)
    # a=es_crud.get_all_docs(index_name=ES_INDEX, size=20)
    # print(a)

    for doc in a:
        all_text = doc['_source']['metadata']['recognized_text'].split(' ')
        words_txt = doc['highlight']['metadata.recognized_text']
        # print(all_text)
        words_detected = []
        for word in words_txt:
            word_detect = ' '.join(re.findall(r"<em>(.*?)</em>", word))
            words_detected.append(word_detect)

        score = doc['_score']
        percent_hostile_to_text = len(words_txt) / len(all_text)
        print(words_detected, len(all_text), len(words_txt), "PERCENT:", percent_hostile_to_text, "_SCORE:", score,"SUM_PERCENT:",score*percent_hostile_to_text)


    print('####################### hostile and less hostile:')
    hostile_query = {
        "query": {
            "match": {"metadata.recognized_text": ' '.join(hostiles_lst)+' '.join(less_hostile_lst)}
        },
        "highlight": {
            "fields": {
                "metadata.recognized_text": {}
            }
        }
    }

    a = es_crud.get_by_query(index_name=ES_INDEX, query=hostile_query, size=20)
    # a=es_crud.get_all_docs(index_name=ES_INDEX, size=20)
    # print(a)

    for doc in a:
        all_text = doc['_source']['metadata']['recognized_text'].split(' ')
        words_txt = doc['highlight']['metadata.recognized_text']
        # print(all_text)
        words_detected = []
        for word in words_txt:
            word_detect = ' '.join(re.findall(r"<em>(.*?)</em>", word))
            words_detected.append(word_detect)

        # score = doc['_score']
        # percent_hostile_to_text = len(words_txt) / len(all_text)
        # print(words_detected, len(all_text), len(words_txt), "PERCENT:", percent_hostile_to_text, "_SCORE:", score,"SUM_PERCENT:",score*percent_hostile_to_text)


        _id = doc['_id']

        # hostile_query = {
        #     "query": {
        #         "match": {"metadata.recognized_text": ' '.join(hostiles_lst) }
        #     },
        #     "highlight": {
        #         "fields": {
        #             "metadata.recognized_text": {}
        #         }
        #     }
        # }


        score_hostile = doc['_score']
        percent_hostile_to_text = len(words_txt) / len(all_text)* 2

        sum_hostile = score_hostile * percent_hostile_to_text

        less_hostile_query = {
            "query": {
                "match": {"metadata.recognized_text": ' '.join(less_hostile_lst),
                          "_id":_id}
            },
            "highlight": {
                "fields": {
                    "metadata.recognized_text": {}
                }
            }
        }

        score_less_hostile = doc['_score']
        percent_less_hostile_to_text = len(words_txt) / len(all_text)

        sum_less_hostile = score_less_hostile * percent_less_hostile_to_text

        sum_sum = sum_hostile + sum_less_hostile

        print(sum_sum)