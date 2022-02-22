from rest_framework import serializers

from .models import Pages


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pages
        # Перечислить все поля, которые могут быть включены в запрос
        # или ответ, включая поля, явно указанные выше.
        fields = ['id', 'name', 'surname', 'otchestvo', 'place_of_birth', 'place_of_death', 'date_of_birth',
                  'date_of_death', 'nationality', 'biography', 'facts', 'avatar', 'pictures', 'videos', 'coords',
                  'price', 'private', 'qr_code']

    def create(self, validated_data):
        return Pages.objects.create_page(**validated_data)
