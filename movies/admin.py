from django.contrib import admin
from django.utils.safestring import mark_safe

from .forms import MovieAdminForm
from .models import (
    Category, Actor, Genre, Movie, MovieShots, RatingStar, Rating, Review)


class ReviewInLines(admin.TabularInline):
    """Отзывы на странице c ..."""
    model = Review
    extra = 1  # кол-во доп. пустых форм
    readonly_fields = ('name', 'email')


class MovieShotsInLines(admin.TabularInline):
    """Кадры из фильма на странице c ..."""
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        """Получение и вывод изображения"""
        return mark_safe(
            f'<img src={obj.image.url} width="auto" height="190">')

    get_image.short_description = 'Кадр из фильма'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ('id', 'name', 'url')
    list_display_links = ('id', 'name')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актёры и режиссёры"""
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        """Вывод изображения, obj - объект модели актёров"""
        return mark_safe(f'<img src={obj.image.url} width="auto" height="80">')

    get_image.short_description = 'Аватарка'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ('name', 'url')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'year')
    search_fields = ('title', 'category__name')  # имя поля связанной модели
    readonly_fields = ('get_image',)
    # Встроить связанные таблицы (m2m/foreignkey)
    inlines = (MovieShotsInLines, ReviewInLines)
    save_on_top = True
    save_as = True  # сохранить как новый объект (для однотипных ообъектов)
    list_editable = ('draft',)
    # fields = (('actors', 'directors', 'genres'),)
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline'),)
        }),
        (None, {
            'fields': ('description', ('poster', 'get_image'))
        }),
        (None, {
            'fields': (('year', 'world_premiere'), 'country')
        }),
        ('Other', {
            'classes': ('collapse',),  # collapse - скрыть поля
            'fields': (('actors', 'directors', 'genres', 'category'),)
        }),
        (None, {
            'fields': (('budget', 'fees_in_usa', 'fess_in_world'),)
        }),
        ('Options', {
            'fields': (('url', 'draft'),)
        }),
    )
    form = MovieAdminForm  # подключение формы (с ckeditor)
    actions = ('publish', 'unpublished')  # регистрация кастомных 'действий'

    def get_image(self, obj):
        """Получение и вывод изображения"""
        return mark_safe(
            f'<img src={obj.poster.url} width="auto" height="120">')

    def publish(self, request, queryset):
        """Опубликовать"""
        # Обновлем все выбранные записи с 'draft=False'
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    def unpublished(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    get_image.short_description = 'Постер'
    publish.short_description = 'Опубликовать'
    # У пользователя должны быть права на изменение 'change' данной записи
    publish.allowed_permissions = ('change',)
    unpublished.short_description = 'Снять с публикации'
    unpublished.allowed_permissions = ('change',)


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ('title', 'movie', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        """Получение и вывод изображения"""
        return mark_safe(f'<img src={obj.image.url} width="auto" height="80">')

    get_image.short_description = 'Кадр из фильма'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ('star', 'movie', 'ip')


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    readonly_fields = ('name', 'email')


admin.site.register(RatingStar)

admin.site.site_title = 'Django Movies'
admin.site.site_header = 'Django Movies'
