from django.urls import path
from . import views


app_name = "catalog"


urlpatterns = [
    path('novel/<slug:public_id>', views.NovelDetailView.as_view(), name='novel-detail'),
    path('chapter/<slug:public_id>', views.ChapterDetailView.as_view(), name='chapter-detail'),
]