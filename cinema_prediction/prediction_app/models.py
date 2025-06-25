from django.db import models

class Movies(models.Model):
    title               = models.CharField(max_length=255)
    prediction          = models.IntegerField(null=True, blank=True)
    release_date        = models.DateField(null=True, blank=True)
    image_url           = models.URLField(max_length=500, null=True, blank=True)
    synospis            = models.TextField(null=True, blank=True)
    casting             = models.TextField(null=True, blank=True)
    # select              = models.BooleanField(default=False)
#     # genre               = models.CharField(max_length=255)  # Format Genre1, Genre2 etc ...
#     # duration            = models.IntegerField(blank=True)
#     # box_office_france   = models.FloatField(null=True, blank=True)
#     # box_office_us       = models.FloatField(null=True, blank=True)
#     # trailer_views       = models.IntegerField(null=True, blank=True)
#     # actor1              = models.CharField(max_length=255, null=True, blank=True)
#     # actor2              = models.CharField(max_length=255, null=True, blank=True)
#     # actor3              = models.CharField(max_length=255, null=True, blank=True)
#     # realisator          = models.CharField(max_length=255, null=True, blank=True)
#     # scenarist           = models.CharField(max_length=255, null=True, blank=True)
#     # distributor         = models.CharField(max_length=255, null=True, blank=True)
#     # production_year     = models.IntegerField(null=True, blank=True)
#     # awards              = models.IntegerField(null=True, blank=True) # tuple [prix,nominations]?
#     # budget              = models.FloatField(null=True, blank=True)
#     # country             = models.CharField(max_length=255, null=True, blank=True)  # Format pays1, pays 2 ...
#     # critics_rating      = models.FloatField(null=True, blank=True)
#     # movie_number        = models.IntegerField(null=True, blank=True)

    # def __str__(self):
    #     return self.title

    # def get_genres(self):
    #     return self.genre.split(',')
    
    # def get_country(self):
    #     return self.country.split(',')



