from django.views.generic import DetailView, CreateView, ListView, UpdateView
from django.shortcuts import get_object_or_404
from .models import Novel, Chapter


class NovelDetailView(DetailView):
    model = Novel
    slug_url_kwarg = "public_id"
    slug_field = "public_id"


class NovelCreateView(CreateView):
    model = Novel
    template_name = 'catalog/novel_form.html'
    fields = [
        'title',
        'format',
        'status',
        'description',
        'release_date',
        'cover',
        'genres',
        'tags',
        'authors',
        'artists',
    ]


class NovelUpdateView(UpdateView):
    model = Novel
    slug_url_kwarg = "public_id"
    slug_field = "public_id"
    fields = [
        'title',
        'format',
        'status',
        'description',
        'release_date',
        'cover',
        'genres',
        'tags',
        'authors',
        'artists',
    ]



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
    

class ChapterCreateView(CreateView):
    model = Chapter
    template_name = 'catalog/chapter_form.html'
    fields = [
        'title',
        'number',
        'content',
    ]

    def form_valid(self, form):
        novel = get_object_or_404(Novel, public_id=self.kwargs.get('public_id'))
        form.instance.novel = novel
        submitted_number = form.cleaned_data.get('number')

        duplicate_exists = Chapter.objects.filter(
            novel=novel, 
            number=submitted_number
        ).exists()

        if duplicate_exists:
            form.add_error('number', f"Chapter {submitted_number} already exists for this novel.")
            return self.form_invalid(form)
        return super().form_valid(form)
    

class NovelListView(ListView):
    model = Novel