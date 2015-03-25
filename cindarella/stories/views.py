from django.views.generic.detail import DetailView
from .models import Variant


class VariantView(DetailView):
    model = Variant
    context_object_name = 'variant'
    template_name = 'stories/variant.html'
