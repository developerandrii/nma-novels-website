from django.views.generic import DetailView
from .models import Novel


class NovelDetailView(DetailView):
    model = Novel
    slug_url_kwarg = "public_id"
    slug_field = "public_id"
