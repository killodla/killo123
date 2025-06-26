import requests

resp = requests.get("https://ecos.bok.or.kr/api/StatisticSearch/sample/json/kr/1/10/722Y001/A/2021/2024/0101000/?/?/?")

resp.json()

print(resp.json())