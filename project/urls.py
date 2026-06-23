from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.core import api, views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("groups/", views.group_list, name="group_list"),
    path("groups/<str:name>/", views.group_detail, name="group_detail"),
    path("fixtures/", views.fixture_list, name="fixture_list"),
    path("matches/<int:pk>/", views.match_detail, name="match_detail"),
    path("matches/<int:pk>/result/", views.save_result, name="save_result"),
    path("bracket/", views.bracket, name="bracket"),
    path("stats/", views.stats, name="stats"),
    path("api/", include(api.router.urls)),
    path("api/matches/<int:pk>/result/", api.MatchResultView.as_view(), name="api_match_result"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
