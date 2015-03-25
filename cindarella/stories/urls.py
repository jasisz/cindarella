from django.conf.urls import url
from .views import VariantView

urlpatterns = [
    url(r'^(?P<story_pk>\d+)/versions/(?P<pk>[\w\d-]+)/$', VariantView.as_view(), name='variant'),
]