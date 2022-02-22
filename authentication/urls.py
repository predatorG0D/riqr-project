from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, CodeCheckAPIView, LogoutAPIView, TokenRefreshView,
    ChangePWDAPIView, ChangeMailAPIView, VerifyEmailAPIView, SupportAPIView, VkAPIView, GoogleAPIView,
    ForgotPasswordAPIView, FeedbackAPIView, MailingAPIView
)

app_name = 'authentication'

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/register/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('users/logout/', LogoutAPIView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('users/code_check/', CodeCheckAPIView.as_view()),
    path('user/change_pwd/', ChangePWDAPIView.as_view()),
    path('user/change_mail/', ChangeMailAPIView.as_view()),
    path('verify_email/', VerifyEmailAPIView.as_view()),
    path('support/', SupportAPIView.as_view()),
    path('oauth/vk/', VkAPIView.as_view()),
    path('oauth/google/', GoogleAPIView.as_view()),
    path('forgot_password/', ForgotPasswordAPIView.as_view()),
    path('feedback/', FeedbackAPIView.as_view()),
    path('mailing/', MailingAPIView.as_view())
]
