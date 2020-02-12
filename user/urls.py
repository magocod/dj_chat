"""
Rutas User
"""

# Django
from django.urls import path

# local Django
from user.views import vauth, vuser, vuserprofile

urlpatterns = [
    # auth
    path("token-auth/", vauth.CustomAuthToken.as_view(), name="user_token_auth",),
    path(
        "jwt-auth/", vauth.AuthJwtHS256Token.as_view(), name="user_jwt_hs_token_auth",
    ),
    path("email/", vauth.EmailView.as_view(), name="user_email_check",),
    path("user/logout/", vauth.LogoutView.as_view(), name="users_logout"),
    # user
    path("users/", vuser.UserListView.as_view(), name="list_users"),
    path("user/<int:pk>/", vuser.UserDetailView.as_view(), name="user_detail",),
    path(
        "user/password/",
        vuser.UserModifyPasswordView.as_view(),
        name="user_modify_password",
    ),
    path(
        "user/profile/",
        vuserprofile.UserProfileView.as_view(),
        name="user_update_profile",
    ),
    path(
        "user/reset_password/",
        vuserprofile.UserPasswordResetView.as_view(),
        name="user_reset_password",
    ),
]
