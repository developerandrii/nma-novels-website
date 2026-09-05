from django.http import Http404
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.db import transaction

from .models import Novel, Chapter, Team, TeamMembership, NovelSubmission


class NovelListView(ListView):
    model = Novel
    queryset = Novel.approved.all()


class NovelDetailView(DetailView):
    model = Novel
    slug_url_kwarg = "public_id"
    slug_field = "public_id"

    def get_object(self, queryset=None):
        novel = super().get_object(queryset)
        user = self.request.user

        # If it's already approved, anyone can view it
        if novel.approval_status == Novel.ApprovalStatus.APPROVED:
            return novel

        # Allow staff/moderators to view pending/rejected novels
        if user.is_authenticated and user.is_staff:
            return novel

        # Allow the original submitter or team member to preview it
        if user.is_authenticated and hasattr(novel, 'submission_request'):
            submission = novel.submission_request
            is_submitter = submission.submitted_by == user
            is_team_member = (
                submission.team and 
                submission.team.memberships.filter(user=user).exists()
            )
            if is_submitter or is_team_member:
                return novel

        # For everyone else, hide it by raising a 404
        raise Http404("No Novel matches the given query.")


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

    def form_valid(self, form):
        user = self.request.user

        # 1. Look up the user's active team (optional - customize to fit your app's active team logic)
        membership = TeamMembership.objects.filter(user=user).first()
        user_team = membership.team if membership else None

        with transaction.atomic():
            novel = form.save(commit=False)
            novel.approval_status = Novel.ApprovalStatus.PENDING
            novel.save()
            
            form.save_m2m()

            NovelSubmission.objects.create(
                novel=novel,
                submitted_by=user,
                team=user_team,
                status=NovelSubmission.Status.PENDING
            )

        return super().form_valid(form)


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


class TeamListView(ListView):
    model = Team


class TeamDetailView(DetailView):
    model = Team
    slug_url_kwarg = "public_id"
    slug_field = "public_id"


class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team
    fields = [
        'name',
        'description',
    ]

    def form_valid(self, form):
            with transaction.atomic():
                self.object = form.save()

                TeamMembership.objects.create(
                    team=self.object,
                    user=self.request.user,
                    role=TeamMembership.Role.OWNER,
                )

            return super().form_valid(form)


