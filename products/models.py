from django.db import models
from slugify import slugify

class Brand(models.Model):
    name = models.CharField(max_length=150, primary_key=True)
    slug = models.SlugField(max_length=150, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Брэнд'
        verbose_name_plural = 'Брэнды'


class SneakersType(models.Model):
    name = models.CharField(max_length=150, primary_key=True)
    slug = models.SlugField(max_length=150, blank=True)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(SneakersType, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class Product(models.Model):
    MALE_CHOICE = (
        ('male', 'Мужские'),
        ('female', 'Женские'),
    )

    SIZE_CHOICE = (
        (36, '36'),
        (37, '37'),
        (38, '38'),
        (39, '39'),
        (40, '40'),
        (41, '41'),
        (42, '42'),
        (43, '43'),
        (44, '44'),
        (45, '45'),
    )

    title = models.CharField(max_length=155)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='product')
    sneakers_type = models.ForeignKey(SneakersType, on_delete=models.CASCADE, related_name='product')
    male = models.CharField(max_length=20, choices=MALE_CHOICE)
    size = models.IntegerField(choices=SIZE_CHOICE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products', null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Кроссовки'
        verbose_name_plural = 'Кроссовки'

