import scrapy
import re
from moviescraper.items import MoviescraperItem

class MoviespiderSpider(scrapy.Spider):
    name = "moviespider"
    allowed_domains = ["www.allocine.fr"]
    start_urls = ["https://www.allocine.fr/films/decennie-2020/"]



    def parse(self, response):
        number_of_pages = int(response.css('div.pagination-item-holder span.button-md.item::text').getall()[-1])
        print('################################')
        print(number_of_pages)
        movies = response.css('div.card.entity-card.entity-card-list.cf')


        for movie in movies:
            title = movie.css('a.meta-title-link ::text').get()
            release_date = movie.css('div.meta-body-item.meta-body-info span.date::text').get()
            duration = movie.css('div.meta-body-item.meta-body-info *::text').getall()[4].strip()
            categories = movie.css('div.meta-body-item.meta-body-info span.dark-grey-link::text').getall()
            realisator = movie.css('div.meta-body-item.meta-body-direction span.dark-grey-link::text').getall()
            actors=movie.css('div.meta-body-item.meta-body-actor span.dark-grey-link::text').getall()
            movie_url =movie.css('a.meta-title-link').attrib['href']
            movie_number = ''.join([x for x in movie_url if x.isdigit()])
            movieItem = MoviescraperItem()
            movieItem['title'] = title,
            movieItem['release_date']=release_date,
            movieItem['duration'] = duration,
            movieItem['categories'] = categories,
            movieItem['realisator_de'] = realisator,
            movieItem['actors']=actors,
            movieItem['movie_number']=movie_number,
            yield response.follow(
                url='https://www.allocine.fr'+movie_url,
                callback= self.parse_movie,
                meta={'item': movieItem}
            )


        for i in range(number_of_pages):
            url_of_the_page = response.url
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print(url_of_the_page)
            if "?" in url_of_the_page:
                next_page_url = url_of_the_page + f'?page={i+2}'
                yield response.follow(next_page_url, callback = self.parse)

            else:
                next_page_url = url_of_the_page + f'?page={i+2}'
                yield response.follow(next_page_url, callback = self.parse)

    def parse_trailer(self, response):
        movie = response.css('div.media-info-item.icon.icon-eye')
        movieItem = response.meta['item']
        trailer_views = movie.css('::text').get().strip()
        movieItem["trailer_views"] = trailer_views
        yield response.follow(
                url='https://www.allocine.fr/film/fichefilm-'+movieItem['movie_number'][0]+'/box-office/',
                callback= self.parse_box_office,
                meta={'item': movieItem}
            )
        

    def parse_movie(self,response):
        movieItem = response.meta['item']
        producer=response.xpath('//div[contains(@class, "meta-body-oneline")]/span[contains(text(), "Par")]/following-sibling::span/text()').getall()
        awards = response.xpath('//div[contains(@class, "item")]/span[contains(text(), "Récompenses")]/following-sibling::span/text()').get(default="").strip()
        country = response.css('section.ovw-technical span.nationality ::text').getall()
        distributor = response.xpath('//div[contains(@class, "item")]/span[contains(text(), "Distributeur")]/following-sibling::span/text()').get()
        trailer_url = response.css('a.trailer.roller-item::attr(href)').get()
        budget = response.xpath('//div[contains(@class, "item")]/span[contains(text(), "Budget")]/following-sibling::span/text()').get()
        annee = response.xpath('//div[contains(@class, "item")]/span[contains(text(), "Année de production")]/following-sibling::span/text()').get()
        critics_rating = response.css('div.rating-holder.rating-holder-3 span.stareval-note ::text').get()
        movieItem['distributor']=distributor
        movieItem['awards']=awards
        movieItem['production_year']=annee
        movieItem['budget'] = budget
        movieItem['country']= country
        movieItem['scenario_par']=producer
        movieItem['critics_rating']=critics_rating
        yield response.follow(
                url='https://www.allocine.fr'+trailer_url,
                callback= self.parse_trailer,
                meta={'item': movieItem}
            )

    def parse_box_office(self, response):
        movieItem = response.meta['item']
        tables = response.css('section.section')
        for index, table in enumerate(tables):
            first_week = table.css('td.responsive-table-column.second-col.col-bg::text').get()
            if first_week:
                n_first_week = first_week.strip().replace(" ", "")
            else:
                n_first_week = ""

            if index == 1:
                France_first_week = n_first_week
            elif index ==2:
                US_first_week = n_first_week
                 
        movieItem['France_first_week'] = France_first_week
        movieItem['US_first_week'] = US_first_week

        yield movieItem  

