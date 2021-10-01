from datetime import date

from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Категории"""
    name = models.CharField(verbose_name='Категория', max_length=150)
    description = models.TextField(verbose_name='Описание')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Actor(models.Model):
    """Актёры и режиссёры"""
    name = models.CharField(verbose_name='Имя', max_length=100)
    age = models.PositiveSmallIntegerField(verbose_name='Возраст', default=0)
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(
        verbose_name='Изображение', upload_to='actors/', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('movies:actor_detail', kwargs={'slug': self.name})

    class Meta:
        verbose_name = 'Актёры и режиссёры'
        verbose_name_plural = 'Актёры и режиссёры'
        ordering = ('name',)


class Genre(models.Model):
    """Жанры"""
    name = models.CharField(verbose_name='Имя', max_length=100)
    description = models.TextField(verbose_name='Описание')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)


class Movie(models.Model):
    """Медиа Файл"""
    title = models.CharField(verbose_name='Название', max_length=100)
    tagline = models.CharField(
        verbose_name='Слоган', max_length=100, default='')
    description = models.TextField(verbose_name='Описание')
    poster = models.ImageField(
        verbose_name='Постер', upload_to='movies/', null=True, blank=True)
    year = models.PositiveSmallIntegerField(
        verbose_name='Дата выхода', default=2021)
    country = models.CharField(verbose_name='Страна', max_length=30)
    directors = models.ManyToManyField(
        Actor, verbose_name='Режиссёр', related_name='film_director')
    actors = models.ManyToManyField(
        Actor, verbose_name='Актёры', related_name='film_actor')
    genres = models.ManyToManyField(Genre, verbose_name='Жанры')
    world_premiere = models.DateField(
        verbose_name='Примьера в мире', default=date.today)
    budget = models.PositiveIntegerField(
        verbose_name='Бюджет', default=0,
        help_text='указывать сумму в долларах')
    fees_in_usa = models.PositiveIntegerField(
        verbose_name='Сборы в США', default=0,
        help_text='указывать сумму в долларах')
    fess_in_world = models.PositiveIntegerField(
        verbose_name='Сборы в мире', default=0,
        help_text='указывать сумму в долларах')
    category = models.ForeignKey(
        Category, verbose_name='Категория', on_delete=models.SET_NULL,
        null=True)
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField(verbose_name='Черновик', default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movies:movie_detail', kwargs={'slug': self.url})

    def get_review(self):
        """
        Список отзывов к данному (self) фильму, c
        пустым полем 'parent' - родительские отзывы
        """
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = 'МедиаФайл'
        verbose_name_plural = 'МедиаФайлы'
        ordering = ('title',)


class MovieShots(models.Model):
    """Кадры из фильма"""
    title = models.CharField(verbose_name='Заголовок', max_length=100)
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(
        verbose_name='Изображение', upload_to='movie_shots/',
        null=True, blank=True)
    movie = models.ForeignKey(
        Movie, verbose_name='Фильм', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кадр из фильма'
        verbose_name_plural = 'Кадры из фильма'
        ordering = ('title',)


class RatingStar(models.Model):
    """Звёзды реётинга"""
    value = models.SmallIntegerField(verbose_name='Значение', default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звёзды рейтинга'
        ordering = ('-value',)


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField(verbose_name='IP адрес', max_length=15)
    star = models.ForeignKey(
        RatingStar, verbose_name='Звезда', on_delete=models.CASCADE)
    movie = models.ForeignKey(
        Movie, verbose_name='Фильм', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.star} - {self.movie}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Review(models.Model):
    """Отзывы"""
    email = models.EmailField(verbose_name='E-mail')
    name = models.CharField(verbose_name='Имя', max_length=100)
    text = models.TextField(verbose_name='Сообщение', max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name='Родитель', on_delete=models.SET_NULL,
        blank=True, null=True)
    movie = models.ForeignKey(
        Movie, verbose_name='Фильм', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
