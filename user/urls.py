"""
Rutas User
"""

# Django
from django.urls import path

# local Django
from user.views import vauth, vuser

urlpatterns = [
    # auth
    path('token-auth/', vauth.CustomAuthToken.as_view(), name='api_token_auth'),
    path('email/', vauth.EmailView.as_view(), name='api_email_check'),
    path('user/logout/', vauth.LogoutView.as_view(), name='api_users_logout'),
    # user
    path('users/', vuser.UserListView.as_view(), name='api_users'),
    path('user/<int:pk>/', vuser.UserDetailView.as_view(), name='api_user_detail'),
]
