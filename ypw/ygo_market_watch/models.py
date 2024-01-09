from django.db import models
from PIL import Image #Pillow Python imaging library


class Card(models.Model):
    Card_name = models.CharField(max_length=255,default='Blue-Eyes White Dragon')
    name_of_set = models.CharField(max_length=255)
    print_tag = models.CharField(max_length=20)
    rarity = models.CharField(max_length=50)
    high_price = models.FloatField()
    low_price = models.FloatField()
    average_price = models.FloatField()
    shift = models.FloatField()
    shift_3 = models.FloatField()
    shift_7 = models.FloatField()
    shift_30 = models.FloatField()
    shift_90 = models.FloatField()
    shift_180 = models.FloatField()
    shift_365 = models.FloatField()
    updated_at = models.DateTimeField()
    card_image = models.ImageField(upload_to='images/', default='images/default_image.jpeg')

    def __str__(self):
        return self.card
    