from scrapy.item import Item, Field


class MoviescraperItem(Item):
    title = Field()
    country = Field()
    duration = Field()
    release_date = Field()
    critics_rating = Field()
    categories = Field()
    realisator_de = Field()
    scenario_par = Field()
    actor1 = Field()
    actor2 = Field()
    actor3 = Field()
    awards=Field()
    budget = Field()
    movie_number=Field()
    France_first_week = Field()
    US_first_week = Field()
    trailer_views = Field()
    production_year=Field()
    distributor=Field()
    sortie_france=Field()


