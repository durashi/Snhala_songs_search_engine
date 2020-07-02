import json

with open('./output.json') as fp:
    data = json.load(fp)

with open('./rubbish.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)