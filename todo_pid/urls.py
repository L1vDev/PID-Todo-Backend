"""
URL configuration for todo_pid project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from functools import lru_cache
from django.conf import settings
from django.utils.translation import gettext as _
from django.conf.urls.static import static

class SeriousSchema(OpenAPISchemaGenerator):
    @lru_cache
    def get_schema(self, request, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ['https'] if request.is_secure() else ['http']
        return schema

schema_view = get_schema_view(
    openapi.Info(
        title=_("Nexus"),
        default_version='v1',
        description=_("TODO"),
        terms_of_service=_('#TODO'),
        contact=openapi.Contact(email="livdev.rguez@gmail.com"),
        license=openapi.License(name="Licensed"),
    ),
    generator_class=SeriousSchema,
    public=settings.DEBUG,
)

urlpatterns = [
    re_path(r'^docs/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^docs/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^docs/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/auth/', include("app_auth.urls")),
    path('api/projects/', include("app_projects.urls")),
    path('api/tasks/', include("app_tasks.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
