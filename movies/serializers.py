from rest_framework import serializers

from .models import Review, Movie, Rating, Actor


class FilterReviewListSerializer(serializers.ListSerializer):
    """Фильтр комментариев, только parents"""

    def to_representation(self, data):
        # data - кверисет => получить все родительские отзывы
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """
    Получение всех записей завязанных на parent.
    Рекурсивный вывод children - дочерних отзывов
    """

    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(
            instance, context=self.context)
        return serializer.data


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Добавление отзыва"""

    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Вывод отзыва"""
    # Рекурсивный вывод отзывов
    children = RecursiveSerializer(many=True)

    class Meta:
        # Фильтрация ответа - вывод только родительских отзывов
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ('id', 'name', 'text', 'children')


class ActorListSerializer(serializers.ModelSerializer):
    """Вывод списка актёров или режиссёров"""

    class Meta:
        model = Actor
        fields = ('id', 'name', 'image')


class ActorDetailSerializer(serializers.ModelSerializer):
    """Вывод полного описания актёра или режиссёра"""

    class Meta:
        model = Actor
        fields = '__all__'


class MovieListSerializer(serializers.ModelSerializer):
    """Список фильмов"""
    # Доп. поле. Логика выполнения определяется во views
    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'tagline', 'category', 'rating_user',
                  'middle_star', 'poster')


class MovieDetailSerializer(serializers.ModelSerializer):
    """Полный вывод фильма"""
    # Вывести данные полей, а не их id
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = ActorListSerializer(read_only=True, many=True)
    actors = ActorListSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(
        slug_field='name', read_only=True, many=True)

    # Доп. поля
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)


class CreateRatingSerializer(serializers.ModelSerializer):
    """Добавление рейтинга пользователем"""

    class Meta:
        model = Rating
        fields = ('star', 'movie')

    def create(self, validated_data):
        # validated_data - данные с клиента
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            # Обновляем/создаём поле star
            defaults={'star': validated_data.get('star')}
        )
        return rating
