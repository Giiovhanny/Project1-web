import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "p7LinRAWJk3A4nnlSb1Ig", "isbns": "9781632168146"})

print(res.json());
console.log('res: ' + JSON.stringify(response))
