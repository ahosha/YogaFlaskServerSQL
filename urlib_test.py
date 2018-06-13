import urllib2
import json
import time

url = 'http://10.0.0.120/api/v1/alignment/get-bands'
headers={'User-agent' : 'Mozilla/5.0'}

for num in range(1,2000):
	try:
		req = urllib2.Request(url, None, headers)
		response = urllib2.urlopen(req).read()
		data = json.loads(response)
		time.sleep(0.3)
		print data
	except URLError, e:
		e.code
		print e.read()