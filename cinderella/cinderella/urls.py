from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView, RedirectView

urlpatterns = [
    # Examples:
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^(?P<story_pk>\d+)/(?P<pk>[\w\d-]+)/$', RedirectView.as_view(pattern_name='stories:mutate'), name='share'),
    url(r'^stories/', include('stories.urls', namespace='stories', app_name='stories')),

    url(r'^admin/', include(admin.site.urls)),
]
