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
    shift = models.DecimalField(max_digits=5, decimal_places=2)
    shift_3 = models.DecimalField(max_digits=5, decimal_places=2)
    shift_7 = models.DecimalField(max_digits=5, decimal_places=2)
    shift_30 = models.DecimalField(max_digits=5, decimal_places=2)
    shift_90 = models.DecimalField(max_digits=5, decimal_places=2)
    shift_180 = models.DecimalField(max_digits=5, decimal_places=2)
    shift_365 = models.DecimalField(max_digits=5, decimal_places=2)
    updated_at = models.DateTimeField()
    card_image = models.ImageField(upload_to='images/', default='images/default_image.jpeg')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.card
    