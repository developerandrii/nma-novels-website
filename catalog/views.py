from django.views.generic import DetailView
from .models import Novel, Chapter


class NovelDetailView(DetailView):
    model = Novel
    slug_url_kwarg = "public_id"
    slug_field = "public_id"



class ChapterDetailView(DetailView):
    model = Chapter
    slug_url_kwarg = "public_id"
    slug_field = "public_id"

    def get_queryset(self):
        return Chapter.objects.select_related("novel")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        chapters = Chapter.objects.filter(
            novel=self.object.novel,
        ).order_by("number")

        context["chapters"] = chapters

        context["previous_chapter"] = (
            chapters
            .filter(number__lt=self.object.number)
            .order_by("-number")
            .first()
        )

        context["next_chapter"] = (
            chapters
            .filter(number__gt=self.object.number)
            .order_by("number")
            .first()
        )

        return context