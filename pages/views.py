import os
from datetime import datetime, timedelta, date
from io import BytesIO
from uuid import uuid4

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from pymediainfo import MediaInfo
import jwt
import qrcode
from PIL import Image
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Pages, Files, Nationalities, Promocode
from .serializers import (
    PageSerializer
)
from authentication.models import User
from django.conf import settings


def filename(x):
    return 'media/' + str(Files.objects.get(id=x).file)


def generate_code(url):
        border = 'staticfiles/qr_code/border.png'
        border = Image.open(border)
        QRcode = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )
        QRcode.add_data(f'https://ritual-front.vercel.app/page/{url}')
        QRcode.make()
        QRimg = QRcode.make_image(
            fill_color="white", back_color="transparent").convert('RGBA')
        basewidth = QRimg.size[0]
        wpercent = (basewidth / float(border.size[0]))
        hsize = int((float(border.size[1]) * float(wpercent)))
        border = border.resize((basewidth, hsize), Image.ANTIALIAS).convert('RGBA')
        qr_code_1 = Image.alpha_composite(border, QRimg).convert('RGB')
        qr_code_2 = Image.alpha_composite(border, QRimg).convert('RGBA')
        qr_code_1.save(settings.MEDIA_ROOT + f"/qr_code/{url}_0.png")
        qr_code_2.save(settings.MEDIA_ROOT + f"/qr_code/{url}_1.png")
        blob1 = BytesIO()
        blob2 = BytesIO()
        qr_code_1.save(blob1, 'png')
        qr_code_2.save(blob2, 'png')
        return File(blob1), File(blob2)


class PageAPIView(APIView):
    serializer_class = PageSerializer

    def get(self, request):
        page = request.GET.get('page')
        page = Pages.objects.get(id=page)
        errors = []
        avatar = None
        try:
            avatar = {'url': 'media/' + str(Files.objects.get(id=page.avatar).file), 'id': page.avatar}
        except ObjectDoesNotExist:
            errors.append({'error': 'Аватар не найден в базе данных'})
        pictures = []
        for i in page.pictures:
            try:
                pictures.append({'url': filename(i), 'id': i})
            except ObjectDoesNotExist:
                errors.append({'error': f'Не удалось загрузить фото из бд: {i}'})
        videos = []
        for i in page.videos:
            try:
                videos.append({'url': filename(i), 'id': i})
            except ObjectDoesNotExist:
                errors.append({'error': f'Не удалось загрузить видео из бд: {i}'})
        qr_codes = []
        for i in page.qr_code:
            try:
                qr_codes.append({'url': filename(i), 'id': i})
            except ObjectDoesNotExist:
                errors.append({'error': f'Не удалось загрузить видео из бд: {i}'})
        my_date = str(page.date_of_creation).split('-')
        time = date(int(my_date[0]), int(my_date[1]), int(my_date[2])) + timedelta(days=3) - datetime.now().date()
        time, _ = divmod(time.total_seconds(), 3600 * 24)
        if time <= 0:
            page.private = True
        nationality = Nationalities.objects.get(id=page.nationality)
        nationality = {'icon': 'staticfiles/nationalities/' + nationality.img, 'name': nationality.country_name,
                       'id': nationality.pk}
        my_page = {"name": page.name,
                   "surname": page.surname,
                   "otchestvo": page.otchestvo,
                   "place_of_birth": page.place_of_birth,
                   "place_of_death": page.place_of_death,
                   "date_of_birth": page.date_of_birth,
                   "date_of_death": page.date_of_death,
                   "nationality": nationality,
                   "biography": page.biography,
                   "facts": page.facts,
                   "avatar": avatar,
                   "pictures": pictures,
                   "videos": videos,
                   "coords": page.coords,
                   "private": page.private,
                   "qr_code": qr_codes}
        if errors:
            response = Response({'erorrs': errors, 'page': my_page}, status=status.HTTP_200_OK)
        else:
            response = Response({'page': my_page}, status=status.HTTP_200_OK)
        return response

    def post(self, request):
        authenticate(request)
        page = request.data.get('page', {})
        serializer = self.serializer_class(data=page)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = request.user
        if str(user) == 'AnonymousUser':
            return Response(status=status.HTTP_403_FORBIDDEN)
        if not user.array_of_pages:
            user.array_of_pages = []
            user.save()
        user.array_of_pages.append(serializer.data['id'])
        user.save()
        photo = []
        for i, file in enumerate(generate_code(serializer.data["id"])):
            instance = Files(file=file, user_id=user.pk)
            instance.file = f'qr_code/{serializer.data["id"]}_{i}.png'
            instance.save()
            photo.append(str(instance.pk))
        page = Pages.objects.get(id=serializer.data['id'])
        page.qr_code = photo
        page.save()
        response = Response({'id': serializer.data['id']}, status=status.HTTP_200_OK)
        return response

    def patch(self, request):
        authenticate(request)
        page = request.data.get('page', {})
        user = request.user
        if str(user) == 'AnonymousUser':
            return Response(status=status.HTTP_403_FORBIDDEN)
        if page.get('id') not in user.array_of_pages:
            return Response({'error': 'Вы не можете редактировать чужую страничку'}, status=status.HTTP_400_BAD_REQUEST)
        page_new = Pages.objects.get(id=page.get('id'))
        page.pop('id')
        for i in page.items():
            setattr(page_new, i[0], i[1])
        page_new.save()
        response = Response(status=status.HTTP_200_OK)
        return response

    def delete(self, request):
        authenticate(request)
        user = request.user
        page = request.GET.get('page')
        if str(user) == 'AnonymousUser':
            return Response(status=status.HTTP_403_FORBIDDEN)
        if page not in user.array_of_pages:
            return Response({'error': 'Вы не можете удалить чужую страничку'}, status=status.HTTP_400_BAD_REQUEST)
        user.array_of_pages.remove(page)
        user.save()
        return Response(status=status.HTTP_200_OK)


class GetUserPagesAPIView(APIView):
    serializer_class = PageSerializer

    def get(self, request):
        authenticate(request)
        user = request.user
        if str(user) == 'AnonymousUser':
            return Response(status=status.HTTP_403_FORBIDDEN)
        pages = []
        for page in user.array_of_pages:
            try:
                instance = Pages.objects.get(id=page)
                my_date = str(instance.date_of_creation).split('-')
                time = date(int(my_date[0]), int(my_date[1]), int(my_date[2])) + timedelta(
                    days=3) - datetime.now().date()
                time, _ = divmod(time.total_seconds(), 3600 * 24)
                if time <= 0:
                    instance.private = True
                try:
                    avatar = Files.objects.get(id=instance.avatar).file
                    pages.append({'id': instance.id, 'price': instance.price, 'avatar': 'media/' + str(avatar),
                                  'name': instance.name, 'surname': instance.surname, 'time_left': int(time),
                                  'private': instance.private, 'payed': instance.payed})
                except ObjectDoesNotExist:
                    pages.append({'id': instance.id, 'price': instance.price, 'avatar': "",
                                  'name': instance.name, 'surname': instance.surname, 'time_left': int(time),
                                  'private': instance.private, 'payed': instance.payed})
            except ObjectDoesNotExist:
                pages.append({'id': page, 'error': 'Не удалось найти страничку в базе данных'})
        response = Response({'pages': pages}, status=status.HTTP_200_OK)
        return response


# def create_preview(file, user_id):
#     try:
#         file_info = MediaInfo.parse(file)
#         is_video = False
#         for track in file_info.tracks:
#             if track.track_type == "Video":
#                 is_video = True
#         if not is_video:
#             return False
#         vidcap = cv.VideoCapture(file)
#         success, image = vidcap.read()
#         if success:
#             name = f"users/{user_id}/" + str(uuid4()) + '.jpg'
#             im = cv.imwrite(os.path.join('media/', name), image)
#             if im:
#                 return name
#             else:
#                 return False
#         return False
#     except:
#         return False


class FilesAPIView(APIView):

    def post(self, request):
        authenticate(request)
        user = request.user
        photo = []
        if str(user) == 'AnonymousUser':
            for filename, file in request.FILES.items():
                instance = Files(file=file, user_id=0)
                instance.save()
                photo.append({'id': str(instance.pk), 'url': 'media/' + str(instance.file)})
            response = Response(photo, status=status.HTTP_200_OK)
            return response
        for filename, file in request.FILES.items():
            instance = Files(file=file, user_id=request.user.pk)
            instance.save()
            photo.append({'id': str(instance.pk), 'url': 'media/' + str(instance.file)})
        response = Response(photo, status=status.HTTP_200_OK)
        return response


class NationalitiesAPIView(APIView):

    def get(self, request):
        nationalities = []
        for i in Nationalities.objects.filter():
            nationalities.append({'icon': 'staticfiles/nationalities/' + i.img, 'name': i.country_name, 'id': i.pk})

        return Response({'nationalities': nationalities}, status=status.HTTP_200_OK)


class PromocodeAPIView(APIView):

    def post(self, request):
        authenticate(request)
        user = request.user
        if str(user) == 'AnonymousUser':
            return Response(status=status.HTTP_403_FORBIDDEN)
        page = request.data.get('page')
        code = request.data.get('code')
        promo = Promocode.objects.get(code=code)
        if promo:
            if not promo.activation_date:
                promo.activation_date = datetime.now()
                promo.user_id = user.pk
                promo.save()
                page = Pages.objects.get(id=page)
                if page.price == 0:
                    return Response({'error': 'Эта страница уже бесплатная'}, status=status.HTTP_400_BAD_REQUEST)
                page.price = 0
                page.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Промокод был активирован'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Промокод не существует'}, status=status.HTTP_400_BAD_REQUEST)
