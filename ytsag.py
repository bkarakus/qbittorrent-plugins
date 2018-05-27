#VERSION: 1.01
from novaprinter import prettyPrinter
from helpers import retrieve_url, download_file
import json

class ytsag(object):
    url = 'https://yts.ag'
    name = 'YTS.AG Torrents'
    supported_categories = {
        'all': '',
        #'movies': 'Comedy',
        'music': 'Music',
        'anime': 'Animation',
    }

    def __init__(self):
        pass

    def search(self, what, cat='all'):
        i = 1
        if 'genre:' in what:
            try:
                what = 'query_term=%s&genre=%s' % (what.split('genre:'))
            except:
                what = 'genre=%s' % (what.replace('genre:',''))
        else:
             what = 'query_term=%s' % (what)
        while True and i<11:
            results = []
            url = self.url+'/api/v2/list_movies.json?sort_by=seeds&limit=50&%s&page=%s' % (what, i)
            json_data = retrieve_url(url)
            try:
                json_dict = json.loads(json_data)
            except:
                i += 1
                continue
            try:
                results = json_dict['data']['movies']
            except KeyError:
                return
            else:
                for r in results:
                    res_dict = dict()
                    res_dict['desc_link'] = r['url']
                    for t in r['torrents']:
                        res_dict['name'] = r['title'] + ' ' + t['quality']
                        res_dict['size'] = t['size']
                        res_dict['seeds'] = t['seeds']
                        res_dict['leech'] = t['peers']
                        res_dict['link'] = t['url']
                        res_dict['engine_url'] = self.url
                        prettyPrinter(res_dict)
            i += 1
                    
if __name__ == "__main__":
    y = ytsag()
    y.search('millers')
