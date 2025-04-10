import scrapy
from moviescraper.items import MoviescraperItem

class MoviespiderSpider(scrapy.Spider):
    name = "moviespider"
    allowed_domains = ["www.allocine.fr"]
    start_urls = ["https://www.allocine.fr/films/decennie-2000/", "https://www.allocine.fr/films/decennie-2010/", "https://www.allocine.fr/films/decennie-2020/"]
    # start_urls=['https://www.allocine.fr/films/alphabetique/decennie-2020/?page=46']


    def parse(self, response):
        # for start_url in self.start_urls:
        number_of_pages = int(response.css('div.pagination-item-holder span.button-md.item::text').getall()[-1])
            # for i in range(1, number_of_pages+1):
        for i in range(1, number_of_pages):
            next_page_url = response.url + f'?page={i}'

            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_page
            )

    
    def parse_page(self, response):
        movies = response.css('div.card.entity-card.entity-card-list.cf')

        for movie in movies:
            title = movie.css('a.meta-title-link ::text').get()
            movieItem = MoviescraperItem()
            duration = movie.css('div.meta-body-item.meta-body-info *::text').getall()[4].strip()
            categories = movie.css('div.meta-body-item.meta-body-info span.dark-grey-link::text').getall()
            categories_item = ""
            for categorie in categories:
                categories_item+=categorie+','
            categories_item=categories_item[:-1]
            realisator = movie.css('div.meta-body-item.meta-body-direction span.dark-grey-link::text').getall()
            actors=movie.css('div.meta-body-item.meta-body-actor span.dark-grey-link::text').getall()
            actors_list = []
            for actor in actors:
                actors_list.append(actor)
            match len(actors_list):
                case 1:
                    movieItem['actor1']=actors_list[0]
                case 2:
                    movieItem['actor1']=actors_list[0]
                    movieItem['actor2']=actors_list[1]
                case 3:
                    movieItem['actor1']=actors_list[0]
                    movieItem['actor2']=actors_list[1]
                    movieItem['actor3']=actors_list[2]
                case _:
                    pass                
            
            movie_url = movie.css('a.meta-title-link').attrib['href']
            movie_number = ''.join([x for x in movie_url if x.isdigit()])
            movieItem['title'] = title
            movieItem['duration'] = duration
            movieItem['categories'] = categories_item
            movieItem['realisator_de'] = realisator
            movieItem['movie_number']=movie_number
            yield response.follow(
                url='https://www.allocine.fr'+movie_url,
                callback= self.parse_movie,
                meta={'item': movieItem}
            )




    def parse_trailer(self, response):
        movie = response.css('div.media-info-item.icon.icon-eye')
        movieItem = response.meta['item']
        if movieItem['sortie_france']:
            trailer_views = movie.css('::text').get().strip()
            movieItem["trailer_views"] = trailer_views
            yield response.follow(
                    url='https://www.allocine.fr/film/fichefilm-'+movieItem['movie_number']+'/box-office/',
                    callback= self.parse_box_office,
                    meta={'item': movieItem}
                )
        else:
            pass
        

    def parse_movie(self,response):
        movieItem = response.meta['item']
        release_date = response.css('div.meta-body-item.meta-body-info span.date ::text').get()
        producer=response.xpath('//div[contains(@class, "meta-body-oneline")]/span[contains(text(), "Par")]/following-sibling::span/text()').getall()
        awards = response.xpath('//div[contains(@class, "item")]/span[contains(text(), "Récompenses")]/following-sibling::span/text()').get(default="").strip()
        country = response.css('section.ovw-technical span.nationality ::text').getall()
        distributor = response.xpath('//div[contains(@class, "item")]/span[contains(text(), "Distributeur")]/following-sibling::span/text()').get()
        trailer_url = response.css('a.trailer.roller-item::attr(href)').get()
        budget = response.xpath('//div[contains(@class, "item")]/span[contains(text(), "Budget")]/following-sibling::span/text()').get()
        annee = response.xpath('//div[contains(@class, "item")]/span[contains(text(), "Année de production")]/following-sibling::span/text()').get()
        sortie_france = True if response.xpath('//div[contains(@class, "item")]/span[contains(text(), "Box Office France")]/following-sibling::span/text()').get()  else False
        critics_rating = response.css('div.rating-holder.rating-holder-3 span.stareval-note ::text').get()
        movieItem['release_date']= release_date
        movieItem['distributor']=distributor
        movieItem['awards']=awards
        movieItem['production_year']=annee
        movieItem['budget'] = budget
        movieItem['country']= country
        movieItem['scenario_par']=producer
        movieItem['critics_rating']=critics_rating
        movieItem['sortie_france']=sortie_france
        if trailer_url:
            yield response.follow(
                    url='https://www.allocine.fr'+trailer_url,
                    callback= self.parse_trailer,
                    meta={'item': movieItem}
                )
        else:
            pass

    def parse_box_office(self, response):
        movieItem = response.meta['item']
        tables= response.css('section.section')

        for table in tables:
            table_box_office = table.css('td.responsive-table-column.second-col.col-bg::text').getall()
            if 'Box Office France' in str(table.getall()):
                if table_box_office:
                    if len(table_box_office)>1:
                        movieItem['France_first_week'] = max(int(table_box_office[0].strip().replace(" ", "")), int(table_box_office[1].strip().replace(" ", "")))
                    else:
                        movieItem['France_first_week']= table_box_office[0].strip().replace(" ","")

            if 'Box Office US' in str(table.getall()):
                if table_box_office:
                    if len(table_box_office)>1:
                        movieItem['US_first_week'] = max(int(table_box_office[0].strip().replace(" ", "")), int(table_box_office[1].strip().replace(" ", "")))
                    else:
                        movieItem['US_first_week']= table_box_office[0].strip().replace(" ","")



        # for index, table in enumerate(tables):
        #     table_box_office = table.css('td.responsive-table-column.second-col.col-bg::text').getall()
        #     if table_box_office:
        #         if len(table_box_office)>1:
        #             n_first_week = max(int(table_box_office[0].strip().replace(" ", "")), int(table_box_office[1].strip().replace(" ", "")))
        #         else:
        #             n_first_week= table_box_office[0].strip().replace(" ","")
        #     else:
        #         n_first_week = ""

        #     if index == 1:
        #         France_first_week = n_first_week
        #     elif index ==2:
        #         US_first_week = n_first_week
                
        # movieItem['France_first_week'] = France_first_week
        # movieItem['US_first_week'] = US_first_week

        yield movieItem
