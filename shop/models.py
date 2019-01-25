from django.db import models
from django.urls import reverse
from utils.storage import ImageStorage
from PIL import Image
from django.conf import settings

import os
from utils.file_size_limit import file_size
from django.core.validators import MinValueValidator


class Category(models.Model):
    catid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])

    def __str__(self):
        return self.name


# make thumbnail
from django.db.models.fields.files import ImageFieldFile

THUMB_ROOT = "products/thumb"


def make_thumb(path, size=280):
    pixbuf = Image.open(path)
    width, height = pixbuf.size

    if width > size:
        delta = width / size
        height = int(height / delta)
        pixbuf.thumbnail((size, height), Image.ANTIALIAS)
        return pixbuf


class Product(models.Model):
    pid = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, db_column='catid', related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, validators=[MinValueValidator(0)])
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', storage=ImageStorage(), validators=[file_size], blank=True,
                              help_text='Please upload the JPG/PNG/GIF format image with size <= 10MB')
    thumb = models.ImageField(blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('pid', 'slug'),)


    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.category.catid, self.category.slug,
                             self.pid, self.slug])

    def __str__(self):
        return self.name

    # save thumbnail
    def save(self):
        super(Product, self).save()
        img_name, extension = os.path.splitext(os.path.basename(self.image.path))
        thumb_pixbuf = make_thumb(os.path.join(settings.MEDIA_ROOT, self.image.name))
        relate_thumb_path = os.path.join(THUMB_ROOT, img_name + '_thumb' + extension)
        thumb_path = os.path.join(settings.MEDIA_ROOT, relate_thumb_path)
        thumb_pixbuf.save(thumb_path)
        self.thumb = ImageFieldFile(self, self.thumb, relate_thumb_path)
        super(Product, self).save()
