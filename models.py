from django.db import models
import datetime

class Category(models.Model):
    title = models.CharField(max_length=200)
    caption = models.CharField(max_length=500)
    color = models.CharField(max_length=6)

    def build_category_dict(self):
        category_dict={}
        category_dict['title'] = self.title
        category_dict['caption'] = self.caption
        category_dict['color'] = self.color
        return category_dict

class Nominee(models.Model):
    title = models.CharField(max_length=500)
    category = models.ForeignKey(Category)
    rating = models.DecimalField(default=1500, max_digits=7, decimal_places=2)
    rating_deviation = models.DecimalField(default=350, max_digits=7, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True, default=datetime.datetime(2000,1,1))

    def build_nominee_dict(self):
        nominee_dict={}
        nominee_dict['title'] = self.title
        nominee_dict['pk'] = self.pk
        return nominee_dict
