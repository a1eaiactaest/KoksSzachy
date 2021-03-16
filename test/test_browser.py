import urllib.request as urlRequest
import urllib.parse as urlParse

url = "https://lichess.org/paste/"
values = {"pgn": '[White "1. platki 2.mleko"]\n[Black "1. mleko 2.platki"]\n\n1. f3 e5 2. g4 Qh4#'}

# pretend to be a chrome 47 browser on a windows 10 machine
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

# encode values for the url
params = urlParse.urlencode(values).encode("utf-8")

# create the url
targetUrl = urlRequest.Request(url=url, data=params, headers=headers)

# open the url
x  = urlRequest.urlopen(targetUrl)

# read the response
respone = x.read()
print(respone)
