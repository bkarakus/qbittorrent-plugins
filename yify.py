from novaprinter import prettyPrinter
from helpers import retrieve_url, download_file
from urllib import quote
from BeautifulSoup import BeautifulSoup

class yify(object):
    url = 'http://yts.re'
    name = 'YIFY'
    supported_categories = {
        'all': 'All',
        'movies': 'Comedy',
        'music': 'Music',
        'anime': 'Animation',
    }

    def __init__(self):
        pass
        
    def search_page(self, what, cat, start):
        results = []
        cat = self.supported_categories[cat]
        url = self.url + '/browse-movie/%s/720p/%s/0/seeds/%s'%(what, cat, start)
        # print url
        html = retrieve_url(url)
        soup = BeautifulSoup(html)
        divs = soup.findAll('div',{'class':'browse-info'})
        for div in divs:
            d = dict()
            info = div.findNext('span',{'class':'info'})
            links = div.findNext('span',{'class':'links'})
            name_span = info.findNext('span',{'class':'browseTitleLink'})
            d['name'] = name_span.text
            size_span = info.findNext('span',{'class':'browseInfoList'})
            d['size'] = size_span.text.replace('Size:','')
            browseSeeds_span = info.findNext('span',{'class':'browseSeeds'})
            leech_span = browseSeeds_span.findNext('span',{'class':'peers'})
            d['leech'] = leech_span.text.replace('Peers:','')
            seeds_span = browseSeeds_span.findNext('span',{'class':'seeds'})
            d['seeds'] = seeds_span.text.replace('Seeds:','')
            desc_link = links.findNext('a')
            d['desc_link'] = desc_link['href']
            d['link'] = desc_link.findNext('a')['href']
            d['engine_url'] = self.url
            results.append(d)
        return results

    def search(self, what, cat='all'):
        start = 1
        f = True
        while f and start < 21:
            page_results = self.search_page(what, cat, start)
            for d in page_results:    
                prettyPrinter(d)
            if len(page_results) < 24:
                f = False
            start += 1
            
if __name__ == "__main__":
    y = yify()
    y.search('cloudy with')