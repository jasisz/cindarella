from django.contrib.sites.models import Site
from django.http.response import HttpResponseRedirect
from django.views.generic.detail import DetailView
from .models import Variant


class VariantView(DetailView):
    model = Variant
    context_object_name = 'variant'
    template_name = 'stories/variant.html'


class MutateView(DetailView):
    model = Variant

    def get(self, request, *args, **kwargs):
        variant = self.get_object()
        mutant = variant.mutate()
        return HttpResponseRedirect(mutant.get_absolute_url())
