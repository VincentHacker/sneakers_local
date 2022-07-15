from django.db import models
from slugify import slugify
from django.contrib.auth import get_user_model

class Brand(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, blank=True, primary_key=True)

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
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, blank=True, primary_key=True)
    
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

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Кроссовки'
        verbose_name_plural = 'Кроссовки'


class Image(models.Model):
    boots = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='boots_image')
    image = models.ImageField(upload_to='products')

    def __str__(self):
        return f'{self.boots}'
    
    class Meta:
        verbose_name = 'Картина'
        verbose_name_plural = 'Картины'


class CommentRating(models.Model):
    rating_choice = (
        (1, '🌟'),
        (2, '🌟🌟'),
        (3, '🌟🌟🌟'),
        (4, '🌟🌟🌟🌟'),
        (5, '🌟🌟🌟🌟🌟'),
    )
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(blank=True, null=True)
    rating = models.IntegerField(choices=rating_choice, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.rating and self.text:
            return f'Comment and rating from {self.author.name} to {self.product}'
        elif self.rating:
            return f'Rating from {self.author.name} to {self.product}'
        elif self.text:
            return f'Comment from {self.author.name} to {self.product}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-create_date']


class Favorites(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')
    favorites = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.author}: favorites {self.product}'

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'

class Like(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='like')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='like')
    like = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.author}: liked {self.product}'

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'