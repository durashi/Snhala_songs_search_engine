from scrapy.spiders import SitemapSpider

class LyricsSpider(SitemapSpider):
    name = "lyrics"
    allowed_domains = ['sinhalasongbook.com']
    sitemap_urls = [
        'https://sinhalasongbook.com//sitemap.xml'
    ]
    sitemap_rules = [('^(?!.*artist).*$', 'parse')]

   
    def parse(self, response):
        song_lines = response.xpath('//*[@id="lyricsBody"]/text()').getall()
        song = ''
        for line in song_lines:
            song_line = line.split('\n')[1].strip()
            song = song + " " + song_line
        yield {
            'title': response.xpath('//*[@id="lyricsTitle"]/h2/text()')[0].get().split(' - ')[0],
            'singer': response.xpath('//*[@id="lyricsTitle"]/h2/text()')[0].get().split(' - ')[1],
            'song' : song
        }
