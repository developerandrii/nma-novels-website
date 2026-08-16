from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from .models import Novel, Chapter


class NovelListView(ListView):
    model = Novel


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


class NovelDeleteView(DeleteView):
    model = Novel
    success_url = reverse_lazy('catalog:novel-list')
    slug_url_kwarg = "public_id"
    slug_field = "public_id"


class NovelSearchView(ListView):
    model = Novel

    def get_queryset(self):
        query = self.request.GET.get('search-novel', '').strip()

        if not query: return None

        queryset = Novel.objects.filter(title__icontains=query)

        if self.request.headers.get('HX-Request'):
            return queryset[:5]
        
        return queryset

    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            return ['catalog/partials/search-dropdown.html']
        
        return ['catalog/novel_list.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the original query string back to populate the search input value
        context['query'] = self.request.GET.get('search', '').strip()
        context['searched_novels'] = self.get_queryset()
        return context



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
    

class ChapterUpdateView(UpdateView):
    model = Chapter
    template_name = 'catalog/chapter_form.html'
    slug_url_kwarg = "public_id"
    slug_field = "public_id"
    fields = [
        'title',
        'number',
        'content',
    ]

    def form_valid(self, form):
        novel = get_object_or_404(Novel, public_id=self.kwargs.get('public_id'))
        form.instance.novel = novel
        return super().form_valid(form)
    

class ChapterDeleteView(DeleteView):
    model = Chapter
    success_url = reverse_lazy('catalog:novel-list')
    slug_url_kwarg = "public_id"
    slug_field = "public_id"

