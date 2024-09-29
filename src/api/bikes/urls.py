# health check
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path  # type: ignore
from rest_framework.routers import DefaultRouter, SimpleRouter

from bikes.views.seasons import SeasonViewSet
from bikes.views.swagger import SwaggerView  # type: ignore

router = SimpleRouter()
router.register(r'seasons', SeasonViewSet, basename='season')

urlpatterns = [
    path("health/", include("health_check.urls")),
    #  path("", ninja_api.urls),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        SwaggerView.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        SwaggerView.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", SwaggerView.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]

print("!!!", router.urls)
urlpatterns += router.urls

urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)