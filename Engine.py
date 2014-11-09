from lxml.html import parse
import urllib3
from urllib.parse import quote_plus

class Engine:

    providers = None
    poolManager = None
    timeout = None
    DEBUG = None

    def __init__(self,timeout=10,debug=False):

        self.poolManager = urllib3.PoolManager(timeout=urllib3.Timeout(timeout),
                                               headers={'Accept-Encoding': 'gzip,deflate'})
        self.DEBUG = debug
                    
    def __complete_url(self,baseUrl,url):
        if url.startswith("/"):
            return baseUrl + url
        return url     
       
    def __query(self,rawUrl,text,category,page,headers=None):
        
        query = quote_plus(text)
        
        url = rawUrl.replace("[text]",query).replace("[category]",category).replace("[page]",str(page))
        if self.DEBUG:
            print(url)
        return  self.poolManager.urlopen('GET',url,preload_content=False,headers=headers)
        
    def __extractData(self,ops,parsed):
        data = {}            
            
        for op,match in ops.items():
            data[op] = []
            container = match["container"]
            for elem in parsed.xpath(match["xpath"]):
                value = None
                if container == "text":
                    try:
                        value = elem.text_content()
                    except UnicodeDecodeError:
                        value = "%UNICODE_ERROR%"
                elif container == "raw":
                    value = str(elem).strip()
                    if value == '':
                        continue
                else:
                    value = elem.attrib[container]
            
                if "replace" in match and len(match["replace"]) == 2:
                    value = value.replace(match["replace"][0],match["replace"][1])

                data[op].append(value);
        
        return data

    def makeQuery(self,provider,text,category,pages,perPageCallback=None,whenDoneCallback=None):
        
        pageRules = provider["pageRules"]
        headers = None
        
        if "replaceInQuery" in provider:
            text = text.replace(provider["replaceInQuery"][0],provider["replaceInQuery"][1])
            
        if "headers" in provider:
            headers = provider["headers"]
        
        for page in range(pageRules["start"],pageRules["start"]+pageRules["step"]*pages,pageRules["step"]):
            resp = self.__query(provider["baseUrl"] + provider["pattern"],text.lower(),provider["categories"][category],page,headers)
            data = self.__extractData(provider["ops"],parse(resp))
            
            isSane,nitems = self.__sanityCheck(data)

            if self.DEBUG and perPageCallback:
                perPageCallback(data,provider["name"],nitems)
            
            if not isSane:
                raise Exception("retrieved data didn't pass the sanity check.")
            
            if not self.DEBUG and perPageCallback:
                perPageCallback(data,provider["name"],nitems)
            
            if nitems < pageRules["maxItems"]:
                break; #Since we fetched all the available data made available by the provider, is pointless to keep going
        
        if whenDoneCallback:
            whenDoneCallback()
            
    def __sanityCheck(self,data):
        
        nitems  = -1
        
        if not "titles" in data or (not "urls" in data and not "magnets" in data):
            return False,nitems
        
        nitems = len(data["titles"])
        
        for key in ["categories","sizes","seeders","leechers","urls","magnets"]:
            if key in data and nitems != len(data[key]):
                return False,nitems
     
        return True,nitems        
        
    def crawl(self,baseUrl,url,crawlerSettings,headers=None):
        if self.DEBUG:
            print("Crawler called for url: '" + url + "'")
        url = self.__complete_url(baseUrl,url)
        resp = self.poolManager.urlopen('GET',url,preload_content=False,headers=headers)
        parsed = parse(resp).xpath(crawlerSettings["xpath"])
        return self.__complete_url(baseUrl,parsed[0].attrib["href"])
        
