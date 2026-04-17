from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from geopram_app import views as geopram_views

custom_admin_patterns = [
    path("", geopram_views.admin_dashboard, name="admin_dashboard"),
    path(
        "major-admin/",
        geopram_views.major_admin_dashboard,
        name="major_admin_dashboard",
    ),
    path(
        "review/<int:verification_id>/",
        geopram_views.admin_review_verification,
        name="admin_review_verification",
    ),
    path(
        "profile/<int:profile_id>/",
        geopram_views.admin_edit_profile,
        name="admin_edit_profile",
    ),
    path(
        "profile/<int:profile_id>/delete/",
        geopram_views.admin_delete_profile,
        name="admin_delete_profile",
    ),
    path("sections/", geopram_views.manage_sections, name="manage_sections"),
    path("sections/create/", geopram_views.create_section, name="create_section"),
]

urlpatterns = [
    path("admin/sections/", geopram_views.manage_sections, name="manage_sections"),
    path("admin/sections/create/", geopram_views.create_section, name="create_section"),
    path(
        "admin/review/<int:verification_id>/",
        geopram_views.admin_review_verification,
        name="admin_review_verification_direct",
    ),
    path(
        "admin/profile/<int:profile_id>/",
        geopram_views.admin_edit_profile,
        name="admin_edit_profile_direct",
    ),
    path("admin/", admin.site.urls),
    path("panel/", include(custom_admin_patterns)),
    path("", include("geopram_app.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
