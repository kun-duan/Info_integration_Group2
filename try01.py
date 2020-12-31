import json
import codecs

data_json = json.load(codecs.open('./static/data/教育部.json', 'r', 'utf-8'))
# print(data_json[0]['loan'])
for i, data in enumerate(data_json):
    print(data['loan'])
