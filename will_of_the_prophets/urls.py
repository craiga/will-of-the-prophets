"""URL configuration."""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

import debug_toolbar

from will_of_the_prophets import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("roll_frequency/", views.roll_frequency, name="roll_frequency"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("roll/", views.RollView.as_view(), name="roll"),
    path("tz_detect/", include("tz_detect.urls")),
    path("s3direct/", include("s3direct.urls")),
    path("", views.public_board, name="public_board"),
]

if settings.DEBUG:
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls))
    ] + urlpatterns
