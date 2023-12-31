from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from military_collections.views import CollectionsViewSet, ContributorsViewSet

router = DefaultRouter()
router.register(r'collections', CollectionsViewSet)
router.register(r'contributors', ContributorsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/contributors/create_contributor/<int:collection_id>/',
         ContributorsViewSet.as_view({'post': 'create_contributor'}),
         name='create_new_contributor'),
    path('api/get-token/', obtain_auth_token),
    path('api/auth/', include('custom_auth.urls'))
]
