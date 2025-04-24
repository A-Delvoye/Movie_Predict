import scrapy
from moviescraper.items import MoviescraperItem

class MovieSpider(scrapy.Spider):
    name = "weekly_spider"
    allowed_domains = ["www.allocine.fr"]
    start_urls = ["https://www.allocine.fr/film/agenda/"]

    def parse(self, response):
        print('#'*50)
        movies = response.css('div.card.entity-card.entity-card-list.cf')

        for movie in movies : 
            title = movie.css('a.meta-title-link ::text').get()
            release_date = movie.css('div.meta-body-item.meta-body-info span.date::text').get()
            categories = movie.css('div.meta-body-item.meta-body-info span.dark-grey-link::text').getall()
            realisator = movie.css('div.meta-body-item.meta-body-direction span.dark-grey-link::text').getall()
            movie_url =movie.css('a.meta-title-link').attrib['href']
            movie_number = ''.join([x for x in movie_url if x.isdigit()])
            movieItem = MoviescraperItem()
            movieItem['title'] = title
            movieItem['release_date']=release_date
            movieItem['categories'] = categories
            movieItem['realisator'] = realisator
            movieItem['movie_number']=movie_number
        
            yield response.follow(
                url='https://www.allocine.fr'+movie_url,
                callback= self.parse_movie,
                meta={'item': movieItem}
            )

    def parse_movie(self,response):
        movieItem = response.meta['item']
        producer=response.xpath('//div[contains(@class, "meta-body-oneline")]/span[contains(text(), "Par")]/following-sibling::span/text()').getall()
        duration = response.xpath('normalize-space(//span[@class="meta-release-type"]/following-sibling::text()[contains(., "h")])').get()
        awards = response.xpath('//div[contains(@class, "item")]/span[contains(text(), "Récompenses")]/following-sibling::span/text()').get(default="").strip()
        country = response.css('section.ovw-technical span.nationality ::text').getall()
        distributor = response.xpath('//div[contains(@class, "item")]/span[contains(text(), "Distributeur")]/following-sibling::span/text()').get()
        budget = response.xpath('//div[contains(@class, "item")]/span[contains(text(), "Budget")]/following-sibling::span/text()').get()
        year = response.xpath('//div[contains(@class, "item")]/span[contains(text(), "Année de production")]/following-sibling::span/text()').get()
        image_url = response.xpath('//img[contains(@class, "thumbnail-img")]/@src').get()
        synospis = response.xpath('//div[contains(@class, "content-txt ")]/p/text()').get()
        trailer_url = response.css('a.trailer.roller-item::attr(href)').get()
        casting_url = response.xpath('//a[contains(@title, "Casting")]/@href').get()
        movieItem['distributor']=distributor
        movieItem['awards']=awards
        movieItem['year']=year
        movieItem['duration'] = duration
        movieItem['budget'] = budget
        movieItem['country']= country
        movieItem['producer']=producer
        movieItem['image_url']=image_url
        movieItem['synospis']=synospis
        movieItem['trailer_url']=trailer_url

        movie_number = movieItem['movie_number']

        if casting_url : 
            yield response.follow(
                url='https://www.allocine.fr/film/fichefilm-'+movie_number+'/casting/',
                callback=self.parse_casting,
                meta={'item': movieItem}
            )
        elif not casting_url and trailer_url:
            yield response.follow(
                url='https://www.allocine.fr'+trailer_url,
                callback=self.parse_trailer,
                meta={'item': movieItem}
                )


    def parse_casting(self, response):

    
        movieItem = response.meta['item']
        trailer_url = movieItem['trailer_url']

        casting1 = response.xpath('//div[contains(@class, "card person-card person-card-col")]//div[@class="meta-title"]/a/text()').getall()
        casting2 = response.css('section.casting-actor div.meta-title span.meta-title-link::text').getall() 

        movieItem['casting'] = casting1+casting2


        if trailer_url : 
            yield response.follow(
                url='https://www.allocine.fr'+trailer_url,
                callback=self.parse_trailer,
                meta={'item': movieItem}
                )
        else:
            yield movieItem
        


    def parse_trailer(self, response):
        movie = response.css('div.media-info-item.icon.icon-eye')
        movieItem = response.meta['item']
        trailer_views = movie.css('::text').get()
        movieItem["trailer_views"] = trailer_views.strip() if trailer_views else None

        yield movieItem  