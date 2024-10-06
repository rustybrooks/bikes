# health check
from django.conf import settings  # type: ignore
from django.conf.urls.static import static  # type: ignore
from django.urls import include, path, re_path  # type: ignore
from rest_framework.routers import SimpleRouter  # type: ignore

from bikes.views.activities import ActivitiesViewSet  # type: ignore
from bikes.views.seasons import SeasonViewSet  # type: ignore
from bikes.views.swagger import SwaggerView  # type: ignore
from bikes.views.users import UserViewSet  # type: ignore

router = SimpleRouter()
router.register(r"api/seasons", SeasonViewSet, basename="season")
router.register(r"api/users", UserViewSet, basename="user")
router.register(r"api/activities", ActivitiesViewSet, basename="activity")

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

urlpatterns += router.urls

urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
