import hashlib
import json
import os
import random
from copy import copy

import requests
import jwt
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from rest_framework import status, views
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Register
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer, LogoutSerializer, TokenRefreshSerializer,
    GoogleSerializer, VkSerializer
)
from django.conf import settings


class RegistrationAPIView(APIView):
    """
    Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту.
    """
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data.get('user', {})

        # Паттерн создания сериализатора, валидации и сохранения - довольно
        # стандартный, и его можно часто увидеть в реальных проектах.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email = serializer.data['email']
        salt = settings.SECRET_KEY
        hashed = hashlib.md5(salt.encode('utf-8') + email.encode('utf-8')).hexdigest()
        new_reg = Register(email=email, hash=hashed, user_id=user.pk)
        new_reg.save()
        link = f'https://ritual-front.vercel.app/verify_email/{hashed}'
        subject = 'Регистрация'
        from_email = 'lev22.08.01@gmail.com'
        text_content = ''
        html_content = """
                <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office" style="width:100%;font-family:'Open Sans', sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0"><head><meta charset="UTF-8"><meta content="width=device-width, initial-scale=1" name="viewport"><meta name="x-apple-disable-message-reformatting"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta content="telephone=no" name="format-detection"><title>Новое письмо 2</title> <!--[if (mso 16)]><style type="text/css">     a {text-decoration: none;}     </style><![endif]--> <!--[if gte mso 9]><style>sup { font-size: 100% !important; }</style><![endif]--> <!--[if gte mso 9]><xml> <o:OfficeDocumentSettings> <o:AllowPNG></o:AllowPNG> <o:PixelsPerInch>96</o:PixelsPerInch> </o:OfficeDocumentSettings> </xml><![endif]--> <!--[if !mso]><!-- --><link href="https://fonts.googleapis.com/css?family=Open+Sans:400,400i,700,700i" rel="stylesheet"><link href="https://fonts.googleapis.com/css?family=Roboto:400,400i,700,700i" rel="stylesheet"> <!--<![endif]--><style type="text/css">#outlook a {	padding:0;}.ExternalClass {	width:100%;}.ExternalClass,.ExternalClass p,.ExternalClass span,.ExternalClass font,.ExternalClass td,.ExternalClass div {	line-height:100%;}.es-button {	mso-style-priority:100!important;	text-decoration:none!important;}a[x-apple-data-detectors] {	color:inherit!important;	text-decoration:none!important;	font-size:inherit!important;	font-family:inherit!important;	font-weight:inherit!important;	line-height:inherit!important;}.es-desk-hidden {	display:none;	float:left;	overflow:hidden;	width:0;	max-height:0;	line-height:0;	mso-hide:all;}[data-ogsb] .es-button {	border-width:0!important;	padding:15px 30px 15px 30px!important;}[data-ogsb] .es-button.es-button-1 {	padding:15px 30px!important;}@media only screen and (max-width:600px) {p, ul li, ol li, a { line-height:150%!important } h1, h2, h3, h1 a, h2 a, h3 a { line-height:120% } h1 { font-size:28px!important; text-align:left } h2 { font-size:20px!important; text-align:left } h3 { font-size:14px!important; text-align:left } h1 a { text-align:left } .es-header-body h1 a, .es-content-body h1 a, .es-footer-body h1 a { font-size:28px!important } h2 a { text-align:left } .es-header-body h2 a, .es-content-body h2 a, .es-footer-body h2 a { font-size:20px!important } h3 a { text-align:left } .es-header-body h3 a, .es-content-body h3 a, .es-footer-body h3 a { font-size:14px!important } .es-menu td a { font-size:14px!important } .es-header-body p, .es-header-body ul li, .es-header-body ol li, .es-header-body a { font-size:14px!important } .es-content-body p, .es-content-body ul li, .es-content-body ol li, .es-content-body a { font-size:14px!important } .es-footer-body p, .es-footer-body ul li, .es-footer-body ol li, .es-footer-body a { font-size:14px!important } .es-infoblock p, .es-infoblock ul li, .es-infoblock ol li, .es-infoblock a { font-size:14px!important } *[class="gmail-fix"] { display:none!important } .es-m-txt-c, .es-m-txt-c h1, .es-m-txt-c h2, .es-m-txt-c h3 { text-align:center!important } .es-m-txt-r, .es-m-txt-r h1, .es-m-txt-r h2, .es-m-txt-r h3 { text-align:right!important } .es-m-txt-l, .es-m-txt-l h1, .es-m-txt-l h2, .es-m-txt-l h3 { text-align:left!important } .es-m-txt-r img, .es-m-txt-c img, .es-m-txt-l img { display:inline!important } .es-button-border { display:block!important } a.es-button, button.es-button { font-size:14px!important; display:block!important; border-bottom-width:20px!important; border-right-width:0px!important; border-left-width:0px!important } .es-btn-fw { border-width:10px 0px!important; text-align:center!important } .es-adaptive table, .es-btn-fw, .es-btn-fw-brdr, .es-left, .es-right { width:100%!important } .es-content table, .es-header table, .es-footer table, .es-content, .es-footer, .es-header { width:100%!important; max-width:600px!important } .es-adapt-td { display:block!important; width:100%!important } .adapt-img { width:100%!important; height:auto!important } .es-m-p0 { padding:0px!important } .es-m-p0r { padding-right:0px!important } .es-m-p0l { padding-left:0px!important } .es-m-p0t { padding-top:0px!important } .es-m-p0b { padding-bottom:0!important } .es-m-p20b { padding-bottom:20px!important } .es-mobile-hidden, .es-hidden { display:none!important } tr.es-desk-hidden, td.es-desk-hidden, table.es-desk-hidden { width:auto!important; overflow:visible!important; float:none!important; max-height:inherit!important; line-height:inherit!important } tr.es-desk-hidden { display:table-row!important } table.es-desk-hidden { display:table!important } td.es-desk-menu-hidden { display:table-cell!important } table.es-table-not-adapt, .esd-block-html table { width:auto!important } table.es-social { display:inline-block!important } table.es-social td { display:inline-block!important } }</style></head>
        <body style="width:100%;font-family:'Open Sans', sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0"><div class="es-wrapper-color" style="background-color:#EFF2F7"> <!--[if gte mso 9]><v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t"> <v:fill type="tile" color="#eff2f7"></v:fill> </v:background><![endif]--><table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-repeat:repeat;background-position:center top"><tr style="border-collapse:collapse"><td valign="top" style="padding:0;Margin:0"><table class="es-content" cellspacing="0" cellpadding="0" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%"><tr style="border-collapse:collapse"><td align="center" style="padding:0;Margin:0"><table class="es-content-body" cellspacing="0" cellpadding="0" bgcolor="#fefefe" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FEFEFE;width:600px"><tr style="border-collapse:collapse"><td align="left" style="padding:0;Margin:0;padding-left:15px;padding-right:15px;padding-top:40px"><table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr style="border-collapse:collapse"><td align="center" valign="top" style="padding:0;Margin:0;width:570px"><table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr style="border-collapse:collapse"><td align="center" style="padding:0;Margin:0;font-size:0px"><img class="adapt-img" src="https://tfjuov.stripocdn.email/content/guids/CABINET_037a4306019ef5c23f502f89087d8fb4/images/final_2_3_pqH.png" alt style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic" width="100"></td>
        </tr><tr style="border-collapse:collapse"><td align="center" style="padding:0;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:roboto, 'helvetica neue', helvetica, arial, sans-serif;line-height:30px;color:#000000;font-size:20px"><strong>Подтвердите адрес своей электронной почты</strong></p></td></tr><tr style="border-collapse:collapse"><td align="center" style="padding:20px;Margin:0;font-size:0"><table border="0" width="100%" height="100%" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr style="border-collapse:collapse"><td style="padding:0;Margin:0;border-bottom:2px solid #cccccc;background:none;height:1px;width:100%;margin:0px"></td></tr></table></td>
        </tr><tr style="border-collapse:collapse"><td align="center" style="padding:0;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:roboto, 'helvetica neue', helvetica, arial, sans-serif;line-height:21px;color:#000000;font-size:14px">Подтвердите адрес электронной почты, чтобы защитить аккаунт.</p></td></tr></table></td></tr></table></td></tr></table></td>
        </tr></table><table cellpadding="0" cellspacing="0" class="es-content" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%"><tr style="border-collapse:collapse"><td align="center" style="padding:0;Margin:0"><table bgcolor="#ffffff" class="es-content-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FEFEFE;width:600px"><tr style="border-collapse:collapse"><td align="left" style="padding:0;Margin:0;padding-left:15px;padding-right:15px;padding-top:20px"><table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr style="border-collapse:collapse"><td align="center" valign="top" style="padding:0;Margin:0;width:570px"><table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr style="border-collapse:collapse"><td align="center" style="padding:0;Margin:0"><span class="es-button-border" style="border-style:solid;border-color:#0C66FF;background:#3939d6;border-width:0px;display:inline-block;border-radius:10px;width:auto"><a href=""" + f"{link}" + """ class="es-button es-button-1" target="_blank" style="mso-style-priority:100 !important;text-decoration:none;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;color:#FFFFFF;font-size:14px;border-style:solid;border-color:#3939d6;border-width:15px 30px;display:inline-block;background:#3939d6;border-radius:10px;font-family:roboto, 'helvetica neue', helvetica, arial, sans-serif;font-weight:bold;font-style:normal;line-height:17px;width:auto;text-align:center">Подтвердить</a></span></td>
        </tr></table></td></tr></table></td></tr></table></td>
        </tr></table><table cellpadding="0" cellspacing="0" class="es-content" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%"><tr style="border-collapse:collapse"><td align="center" style="padding:0;Margin:0"><table bgcolor="#ffffff" class="es-content-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FEFEFE;width:600px"><tr style="border-collapse:collapse"><td align="left" style="padding:0;Margin:0;padding-left:15px;padding-right:15px;padding-top:20px"><table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr style="border-collapse:collapse"><td align="center" valign="top" style="padding:0;Margin:0;width:570px"><table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr style="border-collapse:collapse"><td align="center" style="padding:0;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:roboto, 'helvetica neue', helvetica, arial, sans-serif;line-height:21px;color:#000000;font-size:14px">Или вставьте эту ссылку в адресную строку браузера:&nbsp;<span style="color:#3939d6">""" + f"{link}" + """</span></p>
        </td></tr><tr style="border-collapse:collapse"><td align="center" style="padding:20px;Margin:0;font-size:0"><table border="0" width="100%" height="100%" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr style="border-collapse:collapse"><td style="padding:0;Margin:0;border-bottom:2px solid #cccccc;background:none;height:1px;width:100%;margin:0px"></td></tr></table></td></tr><tr style="border-collapse:collapse"><td align="center" style="padding:0;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:roboto, 'helvetica neue', helvetica, arial, sans-serif;line-height:21px;color:#000000;font-size:14px">Если вы не отправляли запрос на подтверждение почты, то проигнорируйте.<br><br>С уважением,<br>Команда RIQR</p></td></tr></table></td></tr></table></td></tr></table></td>
        </tr></table></td></tr></table></div></body></html>
        """
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        msg.attach_alternative(html_content, "text/html")
        try:
            msg.send()
        except Exception:
            user.delete()
            return Response({'error': 'Не удалось отправить код на вашу почту, попробуйте позже'},
                            status=status.HTTP_400_BAD_REQUEST)
        data = copy(serializer.data)
        data.pop('token')
        response = Response(data, status=status.HTTP_200_OK)
        return response


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        # Обратите внимание, что мы не вызываем метод save() сериализатора, как
        # делали это для регистрации. Дело в том, что в данном случае нам
        # нечего сохранять. Вместо этого, метод validate() делает все нужное.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        data = copy(serializer.data)
        data['access'] = {'value': data['access'],
                          'expires': int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())}
        data['refresh'] = {'value': data['refresh'],
                           'expires': int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds())}
        response = Response(data, status=status.HTTP_200_OK)
        return response


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # Здесь нечего валидировать или сохранять. Мы просто хотим, чтобы
        # сериализатор обрабатывал преобразования объекта User во что-то, что
        # можно привести к json и вернуть клиенту.
        serializer = self.serializer_class(request.user)
        data = copy(serializer.data)
        try:
            data.pop('token')
        except KeyError:
            return Response({'error': 'Auth credentials were not provided'}, status=status.HTTP_400_BAD_REQUEST)
        data['vk'] = bool(data['vk'])
        data['google'] = bool(data['google'])
        data['password'] = bool(serializer.instance.password)
        data['access'] = {'value': serializer.data['token']['access'],
                          'expires': int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())}
        data['refresh'] = {'value': serializer.data['token']['refresh'],
                           'expires': int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds())}
        response = Response(data, status=status.HTTP_200_OK)
        return response

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Паттерн сериализации, валидирования и сохранения - то, о чем говорили
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = copy(serializer.data)
        try:
            data.pop('token')
        except KeyError:
            return Response({'error': 'Auth credentials were not provided'}, status=status.HTTP_400_BAD_REQUEST)
        data['access'] = {'value': serializer.data['token']['access'],
                          'expires': int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())}
        data['refresh'] = {'value': serializer.data['token']['refresh'],
                           'expires': int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds())}
        response = Response(data, status=status.HTTP_200_OK)
        return response


class VerifyEmailAPIView(views.APIView):

    def post(self, request):
        hash = request.data.get('hash')
        try:
            reg = Register.objects.filter(hash=hash)[0]
        except ObjectDoesNotExist:
            return Response({'error': 'Не удалось подтвердить email'}, status=status.HTTP_400_BAD_REQUEST)
        salt = settings.SECRET_KEY
        if hashlib.md5(salt.encode('utf-8') + reg.email.encode('utf-8')).hexdigest() == reg.hash:
            try:
                user = User.objects.get(id=reg.user_id)
                user.verified = True
                user.email = reg.email
                user.save()
            except Exception:
                return Response({'error': 'Пользователь не существует'}, status=status.HTTP_400_BAD_REQUEST)
            reg = Register.objects.filter(hash=hash)
            reg.delete()
            data = dict()
            data['access'] = {'value': user.token['access'],
                              'expires': int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())}
            data['refresh'] = {'value': user.token['refresh'],
                               'expires': int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds())}
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Неверный код'}, status=status.HTTP_400_BAD_REQUEST)


class CodeCheckAPIView(views.APIView):

    def get(self, request):
        user_id = request.GET.get('id', '')
        code = request.GET.get('code', '')
        authenticate(request)
        user = request.user
        if str(user) == 'AnonymousUser':
            if user_id:
                user = User.objects.get(id=user_id)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        if user.code == code:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Неверный код'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data={"refresh": request.data['refresh']})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access', samesite='None')
        response.delete_cookie('refresh', samesite='None')
        return response


class TokenRefreshView(APIView):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """
    serializer_class = TokenRefreshSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {'access': {'value': serializer.data['access'],
                           'expires': int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())},
                'refresh': {'value': serializer.data['refresh'],
                            'expires': int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds())}}
        response = Response(data, status=status.HTTP_200_OK)
        return response


class ChangePWDAPIView(APIView):

    def post(self, request):
        authenticate(request)
        user = request.user
        new_pwd = request.data['user']['new_password']
        if str(user) == 'AnonymousUser':
            user_id = int(request.data['user']['id'])
            code = request.data['user']['code']
            user = User.objects.get(id=user_id)
            if user_id and code and str(code) == str(user.code):
                user.set_password(new_pwd)
                user.code = ""
                user.save()
                response = Response(status=status.HTTP_200_OK)
                return response
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        old_pwd = request.data['user']['old_password']
        if user.check_password(old_pwd):
            user.set_password(new_pwd)
            user.save()
        elif not old_pwd:
            if not user.password:
                user.set_password(new_pwd)
                user.save()
        else:
            return Response({'error': 'Неверный старый пароль'}, status=status.HTTP_400_BAD_REQUEST)
        response = Response(status=status.HTTP_200_OK)
        return response


class ChangeMailAPIView(APIView):

    def post(self, request):
        authenticate(request)
        user = request.user
        if str(user) == 'AnonymousUser':
            return Response(status=status.HTTP_403_FORBIDDEN)
        user.verified = False
        email = request.data['email']
        salt = settings.SECRET_KEY
        hashed = hashlib.md5(salt.encode('utf-8') + email.encode('utf-8')).hexdigest()
        new_reg = Register(email=email, hash=hashed, user_id=user.pk)
        new_reg.save()
        link = f'https://ritual-front.vercel.app/verify_email/{hashed}'
        subject = 'Смена почты'
        from_email = 'lev22.08.01@gmail.com'
        text_content = ''
        html_content = """
                        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office" style="width:100%;font-family:'Open Sans', sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0"><head><meta charset="UTF-8"><meta content="width=device-width, initial-scale=1" name="viewport"><meta name="x-apple-disable-message-reformatting"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta content="telephone=no" name="format-detection"><title>Новое письмо 2</title> <!--[if (mso 16)]><style type="text/css">     a {text-decoration: none;}     </style><![endif]--> <!--[if gte mso 9]><style>sup { font-size: 100% !important; }</style><![endif]--> <!--[if gte mso 9]><xml> <o:OfficeDocumentSettings> <o:AllowPNG></o:AllowPNG> <o:PixelsPerInch>96</o:PixelsPerInch> </o:OfficeDocumentSettings> </xml><![endif]--> <!--[if !mso]><!-- --><link href="https://fonts.googleapis.com/css?family=Open+Sans:400,400i,700,700i" rel="stylesheet"><link href="https://fonts.googleapis.com/css?family=Roboto:400,400i,700,700i" rel="stylesheet"> <!--<![endif]--><style type="text/css">#outlook a {	padding:0;}.ExternalClass {	width:100%;}.ExternalClass,.ExternalClass p,.ExternalClass span,.ExternalClass font,.ExternalClass td,.ExternalClass div {	line-height:100%;}.es-button {	mso-style-priority:100!important;	text-decoration:none!important;}a[x-apple-data-detectors] {	color:inherit!important;	text-decoration:none!important;	font-size:inherit!important;	font-family:inherit!important;	font-weight:inherit!important;	line-height:inherit!important;}.es-desk-hidden {	display:none;	float:left;	overflow:hidden;	width:0;	max-height:0;	line-height:0;	mso-hide:all;}[data-ogsb] .es-button {	border-width:0!important;	padding:15px 30px 15px 30px!important;}[data-ogsb] .es-button.es-button-1 {	padding:15px 30px!important;}@media only screen and (max-width:600px) {p, ul li, ol li, a { line-height:150%!important } h1, h2, h3, h1 a, h2 a, h3 a { line-height:120% } h1 { font-size:28px!important; text-align:left } h2 { font-size:20px!important; text-align:left } h3 { font-size:14px!important; text-align:left } h1 a { text-align:left } .es-header-body h1 a, .es-content-body h1 a, .es-footer-body h1 a { font-size:28px!important } h2 a { text-align:left } .es-header-body h2 a, .es-content-body h2 a, .es-footer-body h2 a { font-size:20px!important } h3 a { text-align:left } .es-header-body h3 a, .es-content-body h3 a, .es-footer-body h3 a { font-size:14px!important } .es-menu td a { font-size:14px!important } .es-header-body p, .es-header-body ul li, .es-header-body ol li, .es-header-body a { font-size:14px!important } .es-content-body p, .es-content-body ul li, .es-content-body ol li, .es-content-body a { font-size:14px!important } .es-footer-body p, .es-footer-body ul li, .es-footer-body ol li, .es-footer-body a { font-size:14px!important } .es-infoblock p, .es-infoblock ul li, .es-infoblock ol li, .es-infoblock a { font-size:14px!important } *[class="gmail-fix"] { display:none!important } .es-m-txt-c, .es-m-txt-c h1, .es-m-txt-c h2, .es-m-txt-c h3 { text-align:center!important } .es-m-txt-r, .es-m-txt-r h1, .es-m-txt-r h2, .es-m-txt-r h3 { text-align:right!important } .es-m-txt-l, .es-m-txt-l h1, .es-m-txt-l h2, .es-m-txt-l h3 { text-align:left!important } .es-m-txt-r img, .es-m-txt-c img, .es-m-txt-l img { display:inline!important } .es-button-border { display:block!important } a.es-button, button.es-button { font-size:14px!important; display:block!important; border-bottom-width:20px!important; border-right-width:0px!important; border-left-width:0px!important } .es-btn-fw { border-width:10px 0px!important; text-align:center!important } .es-adaptive table, .es-btn-fw, .es-btn-fw-brdr, .es-left, .es-right { width:100%!important } .es-content table, .es-header table, .es-footer table, .es-content, .es-footer, .es-header { width:100%!important; max-width:600px!important } .es-adapt-td { display:block!important; width:100%!important } .adapt-img { width:100%!important; height:auto!important } .es-m-p0 { padding:0px!important } .es-m-p0r { padding-right:0px!important } .es-m-p0l { padding-left:0px!important } .es-m-p0t { padding-top:0px!important } .es-m-p0b { padding-bottom:0!important } .es-m-p20b { padding-bottom:20px!important } .es-mobile-hidden, .es-hidden { display:none!important } tr.es-desk-hidden, td.es-desk-hidden, table.es-desk-hidden { width:auto!important; overflow:visible!important; float:none!important; max-height:inherit!important; line-height:inherit!important } tr.es-desk-hidden { display:table-row!important } table.es-desk-hidden { display:table!important } td.es-desk-menu-hidden { display:table-cell!important } table.es-table-not-adapt, .esd-block-html table { width:auto!important } table.es-social { display:inline-block!important } table.es-social td { display:inline-block!important } }</style></head>
                <body style="width:100%;font-family:'Open Sans', sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0"><div class="es-wrapper-color" style="background-color:#EFF2F7"> <!--[if gte mso 9]><v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t"> <v:fill type="tile" color="#eff2f7"></v:fill> </v:background><![endif]--><table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-repeat:repeat;background-position:center top"><tr style="border-collapse:collapse"><td valign="top" style="padding:0;Margin:0"><table class="es-content" cellspacing="0" cellpadding="0" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%"><tr style="border-collapse:collapse"><td align="center" style="padding:0;Margin:0"><table class="es-content-body" cellspacing="0" cellpadding="0" bgcolor="#fefefe" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FEFEFE;width:600px"><tr style="border-collapse:collapse"><td align="left" style="padding:0;Margin:0;padding-left:15px;padding-right:15px;padding-top:40px"><table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr style="border-collapse:collapse"><td align="center" valign="top" style="padding:0;Margin:0;width:570px"><table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr style="border-collapse:collapse"><td align="center" style="padding:0;Margin:0;font-size:0px"><img class="adapt-img" src="https://tfjuov.stripocdn.email/content/guids/CABINET_037a4306019ef5c23f502f89087d8fb4/images/final_2_3_pqH.png" alt style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic" width="100"></td>
                </tr><tr style="border-collapse:collapse"><td align="center" style="padding:0;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:roboto, 'helvetica neue', helvetica, arial, sans-serif;line-height:30px;color:#000000;font-size:20px"><strong>Подтвердите адрес своей электронной почты</strong></p></td></tr><tr style="border-collapse:collapse"><td align="center" style="padding:20px;Margin:0;font-size:0"><table border="0" width="100%" height="100%" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr style="border-collapse:collapse"><td style="padding:0;Margin:0;border-bottom:2px solid #cccccc;background:none;height:1px;width:100%;margin:0px"></td></tr></table></td>
                </tr><tr style="border-collapse:collapse"><td align="center" style="padding:0;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:roboto, 'helvetica neue', helvetica, arial, sans-serif;line-height:21px;color:#000000;font-size:14px">Подтвердите адрес электронной почты, чтобы защитить аккаунт.</p></td></tr></table></td></tr></table></td></tr></table></td>
                </tr></table><table cellpadding="0" cellspacing="0" class="es-content" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%"><tr style="border-collapse:collapse"><td align="center" style="padding:0;Margin:0"><table bgcolor="#ffffff" class="es-content-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FEFEFE;width:600px"><tr style="border-collapse:collapse"><td align="left" style="padding:0;Margin:0;padding-left:15px;padding-right:15px;padding-top:20px"><table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr style="border-collapse:collapse"><td align="center" valign="top" style="padding:0;Margin:0;width:570px"><table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr style="border-collapse:collapse"><td align="center" style="padding:0;Margin:0"><span class="es-button-border" style="border-style:solid;border-color:#0C66FF;background:#3939d6;border-width:0px;display:inline-block;border-radius:10px;width:auto"><a href=""" + f"{link}" + """class="es-button es-button-1" target="_blank" style="mso-style-priority:100 !important;text-decoration:none;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;color:#FFFFFF;font-size:14px;border-style:solid;border-color:#3939d6;border-width:15px 30px;display:inline-block;background:#3939d6;border-radius:10px;font-family:roboto, 'helvetica neue', helvetica, arial, sans-serif;font-weight:bold;font-style:normal;line-height:17px;width:auto;text-align:center">Подтвердить</a></span></td>
                </tr></table></td></tr></table></td></tr></table></td>
                </tr></table><table cellpadding="0" cellspacing="0" class="es-content" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%"><tr style="border-collapse:collapse"><td align="center" style="padding:0;Margin:0"><table bgcolor="#ffffff" class="es-content-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FEFEFE;width:600px"><tr style="border-collapse:collapse"><td align="left" style="padding:0;Margin:0;padding-left:15px;padding-right:15px;padding-top:20px"><table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr style="border-collapse:collapse"><td align="center" valign="top" style="padding:0;Margin:0;width:570px"><table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr style="border-collapse:collapse"><td align="center" style="padding:0;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:roboto, 'helvetica neue', helvetica, arial, sans-serif;line-height:21px;color:#000000;font-size:14px">Или вставьте эту ссылку в адресную строку браузера:&nbsp;<span style="color:#3939d6">""" + f"{link}" + """</span></p>
                </td></tr><tr style="border-collapse:collapse"><td align="center" style="padding:20px;Margin:0;font-size:0"><table border="0" width="100%" height="100%" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr style="border-collapse:collapse"><td style="padding:0;Margin:0;border-bottom:2px solid #cccccc;background:none;height:1px;width:100%;margin:0px"></td></tr></table></td></tr><tr style="border-collapse:collapse"><td align="center" style="padding:0;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:roboto, 'helvetica neue', helvetica, arial, sans-serif;line-height:21px;color:#000000;font-size:14px">Если вы не отправляли запрос на подтверждение почты, то проигнорируйте.<br><br>С уважением,<br>Команда RIQR</p></td></tr></table></td></tr></table></td></tr></table></td>
                </tr></table></td></tr></table></div></body></html>
                """
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        msg.attach_alternative(html_content, "text/html")
        try:
            msg.send()
        except Exception:
            return Response({'error': 'Не удалось отправить код на вашу почту, попробуйте позже'},
                            status=status.HTTP_400_BAD_REQUEST)
        response = Response(status=status.HTTP_200_OK)
        return response


class SupportAPIView(APIView):

    def post(self, request):
        authenticate(request)
        user = request.user
        if str(user) == 'AnonymousUser':
            return Response(status=status.HTTP_403_FORBIDDEN)
        if not user.email:
            return Response({'error': 'Для пользования технической поддержкой укажите email в личном кабинете'},
                            status=status.HTTP_400_BAD_REQUEST)
        email = settings.EMAIL_HOST_USER
        subject = f'[Техническая поддержка] id={user.pk}'
        from_email = 'lev22.08.01@gmail.com'
        text_content = request.data.get(
            'msg') + '\n\n' + f'Контакты для связи: \nemail: {user.email}, telephone_number: {user.telephone_number}'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        try:
            msg.send()
        except Exception:
            return Response({'error': 'Не удалось отправить сообщение, попробуйте позже'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class FeedbackAPIView(APIView):

    def post(self, request):
        authenticate(request)
        user = request.user
        if str(user) == 'AnonymousUser':
            return Response(status=status.HTTP_403_FORBIDDEN)
        email = settings.EMAIL_HOST_USER
        subject = f'[Отзыв] id={user.pk} name={request.data.get("name")}'
        from_email = 'lev22.08.01@gmail.com'
        text_content = request.data.get('msg')
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        try:
            msg.send()
        except Exception:
            return Response({'error': 'Не удалось отправить сообщение, попробуйте позже'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class VkAPIView(APIView):
    serializer_class = VkSerializer

    def get(self, request):
        return Response({
            'url': settings.VK_OAUTH_AUTH})

    def post(self, request):
        code = request.data.get('code')
        res = json.loads(requests.get(settings.VK_OAUTH_TOKEN + str(code)).text)
        if res.get('error') is not None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        authenticate(request)
        user = request.user
        if str(user) != 'AnonymousUser':
            try:
                user = User.objects.get(vk=res.get('user_id'))
            except ObjectDoesNotExist:
                user.vk = res.get('user_id')
                user.access_vk = res.get('access_token')
                user.save()
            else:
                return Response({'error': f'Другой пользователь уже привязал этот вк'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user = User.objects.get(vk=res.get('user_id'))
            except ObjectDoesNotExist:
                try:
                    user = User.objects.get(email=res.get('email'))
                    user.vk = res.get('user_id')
                    user.access_vk = res.get('access_token')
                    user.verified = True
                    user.save()
                except ObjectDoesNotExist:
                    user = User(vk=res.get('user_id'), email=res.get('email'), access_vk=res.get('access_token'),
                                verified=True)
                    user.save()
                    user.username = f'user{1000000 + user.pk}'
                    user.save()
        serializer = self.serializer_class(data={"vk": user.vk})
        serializer.is_valid(raise_exception=True)
        data = {'access': {'value': serializer.data['access'],
                           'expires': int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())},
                'refresh': {'value': serializer.data['refresh'],
                            'expires': int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds())}}
        response = Response(data, status=status.HTTP_200_OK)
        return response


class GoogleAPIView(APIView):
    serializer_class = GoogleSerializer

    def get(self, request):
        return Response({
            'url': settings.GOOGLE_OAUTH_AUTH})

    def post(self, request):
        code = request.data.get('code')
        url = requests.post(settings.GOOGLE_OAUTH_TOKEN + str(code))
        text = url.text
        res = json.loads(text)
        if res.get('error') is not None:
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        google_jwt = res.get('id_token')
        id_token = jwt.decode(google_jwt, options={"verify_signature": False})
        authenticate(request)
        user = request.user
        if str(user) != 'AnonymousUser':
            try:
                user = User.objects.get(google=id_token.get('sub'))
            except ObjectDoesNotExist:
                user.google = id_token.get('sub')
                user.access_google = res.get('access_token')
                user.save()
            else:
                return Response({'error': 'Другой пользователь уже привязал этот google'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user = User.objects.get(google=id_token.get('sub'))
            except ObjectDoesNotExist:
                try:
                    user = User.objects.get(email=id_token.get('email'))
                    user.google = id_token.get('sub')
                    user.access_google = res.get('access_token')
                    user.verified = True
                    user.save()
                except ObjectDoesNotExist:
                    user = User(google=id_token.get('sub'), email=id_token.get('email'),
                                access_google=res.get('access_token'), verified=True)
                    user.save()
                    user.username = f'user{1000000 + user.pk}'
                    user.save()
        serializer = self.serializer_class(data={"google": user.google})
        serializer.is_valid(raise_exception=True)
        data = {'access': {'value': serializer.data['access'],
                           'expires': int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())},
                'refresh': {'value': serializer.data['refresh'],
                            'expires': int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds())}}
        response = Response(data, status=status.HTTP_200_OK)
        return response


class ForgotPasswordAPIView(APIView):

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.get(email=email)
        if not user:
            return Response({'error': 'Пользователя с данным email не существует'}, status=status.HTTP_400_BAD_REQUEST)
        subject = 'Смена пароля'
        code = random.randint(0, 999999)
        code = str(code).zfill(6)
        user.code = code
        user.save()
        from_email = 'lev22.08.01@gmail.com'
        text_content = ''
        html_content = """
                                <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office" style="width:100%;font-family:'Open Sans', sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0"><head><meta charset="UTF-8"><meta content="width=device-width, initial-scale=1" name="viewport"><meta name="x-apple-disable-message-reformatting"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta content="telephone=no" name="format-detection"><title>Новое письмо 2</title> <!--[if (mso 16)]><style type="text/css">     a {text-decoration: none;}     </style><![endif]--> <!--[if gte mso 9]><style>sup { font-size: 100% !important; }</style><![endif]--> <!--[if gte mso 9]><xml> <o:OfficeDocumentSettings> <o:AllowPNG></o:AllowPNG> <o:PixelsPerInch>96</o:PixelsPerInch> </o:OfficeDocumentSettings> </xml><![endif]--> <!--[if !mso]><!-- --><link href="https://fonts.googleapis.com/css?family=Open+Sans:400,400i,700,700i" rel="stylesheet"><link href="https://fonts.googleapis.com/css?family=Roboto:400,400i,700,700i" rel="stylesheet"> <!--<![endif]--><style type="text/css">#outlook a {	padding:0;}.ExternalClass {	width:100%;}.ExternalClass,.ExternalClass p,.ExternalClass span,.ExternalClass font,.ExternalClass td,.ExternalClass div {	line-height:100%;}.es-button {	mso-style-priority:100!important;	text-decoration:none!important;}a[x-apple-data-detectors] {	color:inherit!important;	text-decoration:none!important;	font-size:inherit!important;	font-family:inherit!important;	font-weight:inherit!important;	line-height:inherit!important;}.es-desk-hidden {	display:none;	float:left;	overflow:hidden;	width:0;	max-height:0;	line-height:0;	mso-hide:all;}[data-ogsb] .es-button {	border-width:0!important;	padding:15px 30px 15px 30px!important;}[data-ogsb] .es-button.es-button-1 {	padding:15px 30px!important;}@media only screen and (max-width:600px) {p, ul li, ol li, a { line-height:150%!important } h1, h2, h3, h1 a, h2 a, h3 a { line-height:120% } h1 { font-size:28px!important; text-align:left } h2 { font-size:20px!important; text-align:left } h3 { font-size:14px!important; text-align:left } h1 a { text-align:left } .es-header-body h1 a, .es-content-body h1 a, .es-footer-body h1 a { font-size:28px!important } h2 a { text-align:left } .es-header-body h2 a, .es-content-body h2 a, .es-footer-body h2 a { font-size:20px!important } h3 a { text-align:left } .es-header-body h3 a, .es-content-body h3 a, .es-footer-body h3 a { font-size:14px!important } .es-menu td a { font-size:14px!important } .es-header-body p, .es-header-body ul li, .es-header-body ol li, .es-header-body a { font-size:14px!important } .es-content-body p, .es-content-body ul li, .es-content-body ol li, .es-content-body a { font-size:14px!important } .es-footer-body p, .es-footer-body ul li, .es-footer-body ol li, .es-footer-body a { font-size:14px!important } .es-infoblock p, .es-infoblock ul li, .es-infoblock ol li, .es-infoblock a { font-size:14px!important } *[class="gmail-fix"] { display:none!important } .es-m-txt-c, .es-m-txt-c h1, .es-m-txt-c h2, .es-m-txt-c h3 { text-align:center!important } .es-m-txt-r, .es-m-txt-r h1, .es-m-txt-r h2, .es-m-txt-r h3 { text-align:right!important } .es-m-txt-l, .es-m-txt-l h1, .es-m-txt-l h2, .es-m-txt-l h3 { text-align:left!important } .es-m-txt-r img, .es-m-txt-c img, .es-m-txt-l img { display:inline!important } .es-button-border { display:block!important } a.es-button, button.es-button { font-size:14px!important; display:block!important; border-bottom-width:20px!important; border-right-width:0px!important; border-left-width:0px!important } .es-btn-fw { border-width:10px 0px!important; text-align:center!important } .es-adaptive table, .es-btn-fw, .es-btn-fw-brdr, .es-left, .es-right { width:100%!important } .es-content table, .es-header table, .es-footer table, .es-content, .es-footer, .es-header { width:100%!important; max-width:600px!important } .es-adapt-td { display:block!important; width:100%!important } .adapt-img { width:100%!important; height:auto!important } .es-m-p0 { padding:0px!important } .es-m-p0r { padding-right:0px!important } .es-m-p0l { padding-left:0px!important } .es-m-p0t { padding-top:0px!important } .es-m-p0b { padding-bottom:0!important } .es-m-p20b { padding-bottom:20px!important } .es-mobile-hidden, .es-hidden { display:none!important } tr.es-desk-hidden, td.es-desk-hidden, table.es-desk-hidden { width:auto!important; overflow:visible!important; float:none!important; max-height:inherit!important; line-height:inherit!important } tr.es-desk-hidden { display:table-row!important } table.es-desk-hidden { display:table!important } td.es-desk-menu-hidden { display:table-cell!important } table.es-table-not-adapt, .esd-block-html table { width:auto!important } table.es-social { display:inline-block!important } table.es-social td { display:inline-block!important } }</style></head>
<body style="width:100%;font-family:'Open Sans', sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0"><div class="es-wrapper-color" style="background-color:#EFF2F7"> <!--[if gte mso 9]><v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t"> <v:fill type="tile" color="#eff2f7"></v:fill> </v:background><![endif]--><table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-repeat:repeat;background-position:center top"><tr style="border-collapse:collapse"><td valign="top" style="padding:0;Margin:0"><table class="es-content" cellspacing="0" cellpadding="0" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%"><tr style="border-collapse:collapse"><td align="center" style="padding:0;Margin:0"><table class="es-content-body" cellspacing="0" cellpadding="0" bgcolor="#fefefe" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FEFEFE;width:600px"><tr style="border-collapse:collapse"><td align="left" style="padding:0;Margin:0;padding-left:15px;padding-right:15px;padding-top:40px"><table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr style="border-collapse:collapse"><td align="center" valign="top" style="padding:0;Margin:0;width:570px"><table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr style="border-collapse:collapse"><td align="center" style="padding:0;Margin:0;font-size:0px"><img class="adapt-img" src="https://tfjuov.stripocdn.email/content/guids/CABINET_037a4306019ef5c23f502f89087d8fb4/images/final_2_3_pqH.png" alt style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic" width="100"></td>
</tr><tr style="border-collapse:collapse"><td align="center" style="padding:0;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:roboto, 'helvetica neue', helvetica, arial, sans-serif;line-height:30px;color:#000000;font-size:20px"><strong>Смена пароля</strong></p></td></tr><tr style="border-collapse:collapse"><td align="center" style="padding:20px;Margin:0;font-size:0"><table border="0" width="100%" height="100%" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr style="border-collapse:collapse"><td style="padding:0;Margin:0;border-bottom:2px solid #cccccc;background:none;height:1px;width:100%;margin:0px"></td></tr></table></td>
</tr><tr style="border-collapse:collapse"><td align="center" style="padding:0;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:roboto, 'helvetica neue', helvetica, arial, sans-serif;line-height:21px;color:#000000;font-size:14px">Введите код, чтобы сменить пароль</p></td></tr></table></td></tr></table></td></tr></table></td>
</tr></table><table cellpadding="0" cellspacing="0" class="es-content" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%"><tr style="border-collapse:collapse"><td align="center" style="padding:0;Margin:0"><table bgcolor="#ffffff" class="es-content-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FEFEFE;width:600px"><tr style="border-collapse:collapse"><td align="left" style="padding:0;Margin:0;padding-left:15px;padding-right:15px;padding-top:20px"><table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr style="border-collapse:collapse"><td align="center" valign="top" style="padding:0;Margin:0;width:570px"><table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr style="border-collapse:collapse"><td align="center" style="padding:0;Margin:0"><span class="es-button-border" style="border-style:solid;border-color:#0C66FF;background:#3939d6;border-width:0px;display:inline-block;border-radius:10px;width:auto"><a class="es-button es-button-1" target="_blank" style="mso-style-priority:100 !important;text-decoration:none;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;color:#FFFFFF;font-size:14px;border-style:solid;border-color:#3939d6;border-width:15px 30px;display:inline-block;background:#3939d6;border-radius:10px;font-family:roboto, 'helvetica neue', helvetica, arial, sans-serif;font-weight:bold;font-style:normal;line-height:17px;width:auto;text-align:center">""" + f"{code}" + """</a></span></td>
</tr></table></td></tr></table></td></tr></table></td>
</tr></table><table cellpadding="0" cellspacing="0" class="es-content" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%"><tr style="border-collapse:collapse"><td align="center" style="padding:0;Margin:0"><table bgcolor="#ffffff" class="es-content-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FEFEFE;width:600px"><tr style="border-collapse:collapse"><td align="left" style="padding:0;Margin:0;padding-left:15px;padding-right:15px;padding-top:20px"><table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr style="border-collapse:collapse"><td align="center" valign="top" style="padding:0;Margin:0;width:570px"><table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr style="border-collapse:collapse"><td align="center" style="padding:0;Margin:0">
</td></tr><tr style="border-collapse:collapse"><td align="center" style="padding:20px;Margin:0;font-size:0"><table border="0" width="100%" height="100%" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr style="border-collapse:collapse"><td style="padding:0;Margin:0;border-bottom:2px solid #cccccc;background:none;height:1px;width:100%;margin:0px"></td></tr></table></td></tr><tr style="border-collapse:collapse"><td align="center" style="padding:0;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:roboto, 'helvetica neue', helvetica, arial, sans-serif;line-height:21px;color:#000000;font-size:14px">Если вы не отправляли запрос на подтверждение почты, то проигнорируйте.<br><br>С уважением,<br>Команда RIQR</p></td></tr></table></td></tr></table></td></tr></table></td>
</tr></table></td></tr></table></div></body></html>
                        """
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        msg.attach_alternative(html_content, "text/html")
        try:
            msg.send()
        except Exception:
            return Response({'error': 'Не удалось отправить код на вашу почту, попробуйте позже'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'user_id': user.pk}, status=status.HTTP_200_OK)


class MailingAPIView(APIView):

    def patch(self, request):
        authenticate(request)
        user = request.user
        if str(user) == 'AnonymousUser':
            return Response(status=status.HTTP_403_FORBIDDEN)
        allow_promotion = request.data.get("allow_promotion", '')
        if allow_promotion is not '':
            user.allow_promotion = allow_promotion
        allow_useful_information = request.data.get("allow_useful_information", '')
        if allow_useful_information is not '':
            user.allow_useful_information = allow_useful_information
        allow_new_things = request.data.get("allow_new_things", '')
        if allow_new_things is not '':
            user.allow_new_things = allow_new_things
        allow_suspicious = request.data.get("allow_suspicious", '')
        if allow_suspicious is not '':
            user.allow_suspicious = allow_suspicious
        allow_unidentified = request.data.get("allow_unidentified", '')
        if allow_unidentified is not '':
            user.allow_unidentified = allow_unidentified
        remind_after = request.data.get("remind_after", '')
        if remind_after is not '':
            user.remind_after = int(remind_after)
        user.save()
        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        authenticate(request)
        user = request.user
        if str(user) == 'AnonymousUser':
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(data={
            "allow_promotion": user.allow_promotion,
            "allow_useful_information": user.allow_useful_information,
            "allow_new_things": user.allow_new_things,
            "allow_suspicious": user.allow_suspicious,
            "allow_unidentified": user.allow_unidentified,
            "remind_after": user.remind_after
        }, status=status.HTTP_200_OK)