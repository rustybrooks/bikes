from drf_yasg import openapi  # type: ignore
from drf_yasg.views import get_schema_view  # type: ignore
from rest_framework.permissions import AllowAny  # type: ignore

# class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
#     def __init__(self, info, version="", url=None, patterns=None, urlconf=None):
#         super().__init__(info, version, url, patterns, urlconf)
#
#     def get_schema(self, *args, **kwargs):
#         schema = super().get_schema(*args, **kwargs)
#
#         if "CUSTOMER_NAME" in os.environ:
#             schema.schemes = ["https"]
#             schema.host = f'{os.environ["CUSTOMER_NAME"]}.hubble.cloud'
#             schema.basePath = "/api/v3"
#
#         return schema


api_info = openapi.Info(
    title="Bikes API",
    default_version="v1",
)

SwaggerView = get_schema_view(
    info=api_info,
    public=True,
    permission_classes=[AllowAny],
    # generator_class=CustomOpenAPISchemaGenerator,
)
