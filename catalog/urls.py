from django.urls import path
from . import views


app_name = "catalog"


urlpatterns = [
    path('novels/', views.NovelListView.as_view(), name='novel-list'),
    path('novel/add/', views.NovelCreateView.as_view(), name='novel-create'),
    path('novel/<slug:public_id>/', views.NovelDetailView.as_view(), name='novel-detail'),
    path('novel/<slug:public_id>/update/', views.NovelUpdateView.as_view(), name='novel-update'),
    path('novel/<slug:public_id>/delete/', views.NovelDeleteView.as_view(), name='novel-delete'),
    path('search/', views.NovelSearchView.as_view(), name='novel-search'),

    path('novel/<slug:public_id>/add/', views.ChapterCreateView.as_view(), name='chapter-add'),
    path('chapter/<slug:public_id>/', views.ChapterDetailView.as_view(), name='chapter-detail'),
    path('chapter/<slug:public_id>/update/', views.ChapterUpdateView.as_view(), name='chapter-update'),
    path('chapter/<slug:public_id>/delete/', views.ChapterDeleteView.as_view(), name='chapter-delete'),

    path('tems/', views.TeamListView.as_view(), name='team-list'),
    path('tems/add/', views.TeamCreateView.as_view(), name='team-create'),
    path('tems/<slug:public_id>/', views.TeamDetailView.as_view(), name='team-detail'),

]