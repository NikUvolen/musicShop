from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class MediaType(models.Model):
    """Модель медианосителя"""

    name = models.CharField(max_length=100, verbose_name='Название медианосителя')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Медианоситель'
        verbose_name_plural = 'Медианосители'


class Member(models.Model):
    """Музыкант (член группы)"""

    name = models.CharField(max_length=255, verbose_name='Имя музыканта')
    slug = models.SlugField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Музыкант'
        verbose_name_plural = 'Музыканты'


class Genre(models.Model):
    """Музыкальный жанр"""

    name = models.CharField(max_length=50, verbose_name='Название жанра')
    slug = models.SlugField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Artist(models.Model):
    """Исполнитель"""

    name = models.CharField(max_length=255, verbose_name='Исполнитель/группа')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    members = models.ManyToManyField(Member, verbose_name='Участник', related_name='artist')
    slug = models.SlugField()

    def __str__(self):
        return f'{self.name} | {self.genre.name}'

    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'


class Album(models.Model):
    """Альбом  исполнителя"""

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, verbose_name='Исполнитель')
    name = models.CharField(max_length=255, verbose_name='Название альбома')
    media_type = models.ForeignKey(MediaType, verbose_name='Носитель', on_delete=models.CASCADE)
    songs_list = models.TextField(verbose_name='Треклист')
    release_date = models.DateField(verbose_name='Дата релиза')
    slug = models.SlugField()
    description = models.TextField(verbose_name='Описание', default='Описание появится позже')
    stock = models.IntegerField(default=0, verbose_name='Наличие на складе')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    offer_of_the_week = models.BooleanField(default=False, verbose_name='Является ли предложением недели')

    def __str__(self):
        return f'{self.pk} | {self.artist.name} | {self.name}'

    @property
    def ct_model(self):
        return self._meta.model_name

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'


class CartProduct(models.Model):
    """Продукт корзины"""

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_type = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)  # col-vo
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')
