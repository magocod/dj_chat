"""djrepo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from rest_framework.permissions import AllowAny
from rest_framework.schemas import get_schema_view

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

# urls api
from apps.user.urls import urlpatterns as user_urls

# concat routes
API_URLS = user_urls

urlpatterns = [
    # docs
    path(
        "openapi/",
        get_schema_view(
            title="djchat",
            description="Websockets",
            version="1.0.0",
            permission_classes=(AllowAny,),
            public=True,
        ),
        name="openapi-schema",
    ),
    path(
        "swagger-ui/",
        TemplateView.as_view(
            template_name="swagger-ui.html",
            extra_context={"schema_url": "openapi-schema"},
        ),
        name="swagger-ui",
    ),
    path(
        "redoc/",
        TemplateView.as_view(
            template_name="redoc.html", extra_context={"schema_url": "openapi-schema"}
        ),
        name="redoc",
    ),
    # web
    path("", TemplateView.as_view(template_name="index.html")),
    path("admin/", admin.site.urls),
    # api
    path("api/", include(API_URLS)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
