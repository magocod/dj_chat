"""
Rutas User
"""

# Django
from django.urls import path

# local Django
from apps.user.views import vauth, vuser

urlpatterns = [
    # auth
    path('token-auth/', vauth.CustomAuthToken.as_view(), name='api_token_auth'),
    path('email/', vauth.VEmail.as_view(), name='api_email_check'),
    path('user/logout/', vauth.VLogout.as_view(), name='api_users_logout'),
    # user
    path('users/', vuser.VUserList.as_view(), name='api_users'),
    path('user/<int:pk>/', vuser.VUserDetail.as_view(), name='api_user_detail'),
]
