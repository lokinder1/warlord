
import requests, re
from  bs4 import BeautifulSoup
from functools import partial
from multiprocessing import Pool
 
#url
class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'

	def disable(self):
		self.HEADER = ''
		self.OKBLUE = ''
		self.OKGREEN = ''
		self.WARNING = ''
		self.FAIL = ''
		self.ENDC = ''

def get_urls(search_string, start):
	url = 'http://www.google.com/search'

	temp=[]	
		 
	#Parameters in payload
	payload = { 'q' : search_string , 'start' : start }
	 
	#Setting User-Agent
	my_headers = { 'User-agent' : 'Mozilla/11.0' }
	 
	#Getting the response in an Object r
	r = requests.get( url, params = payload, headers = my_headers )
	 
	#Create a Beautiful soup Object of the response r parsed as html
	soup = BeautifulSoup( r.text, 'html.parser' )
	 
	#Getting all h3 tags with class 'r'
	h3tags = soup.find_all( 'h3', class_='r' )
	 
	#Finding URL inside each h3 tag using regex.
	#If found : Print, else : Ignore the exception
	for h3 in h3tags:
		try:
			temp.append( re.search('url\?q=(.+?)\&sa', h3.a['href']).group(1))
		except:
			continue
	return temp
	 
	#End

def dork_scanner(search, pages, processes):

	result = []
	#arguments = docopt(__doc__,version='warlord google dork mass exploiter')
	search=search
	pages=pages
	proce=int(processes)
	
	make_request = partial(get_urls,search)
	pagelist     = [str(x*10) for x in range(0,int(pages))]
	with Pool(proce) as p:
		tmp=p.map(make_request, pagelist)
	for x in tmp:
		result.extend(x)	
	i=0
	result =list(set(result))
	return result
