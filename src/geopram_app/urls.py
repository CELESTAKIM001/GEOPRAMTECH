from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("software/", views.software, name="software"),
    path("solutions/", views.solutions, name="solutions"),
    path("training/", views.training, name="training"),
    path("terms/", views.terms, name="terms"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("contact/", views.contact, name="contact"),
    path("register/", views.register, name="register"),
    path("profile/create/", views.profile_create, name="profile_create"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("skill/add/", views.add_skill, name="add_skill"),
    path("item/add/", views.add_item, name="add_item"),
    path(
        "verify/request/<str:item_type>/<int:item_id>/",
        views.request_verification,
        name="request_verification",
    ),
    path("admin/", views.admin_dashboard, name="admin_dashboard"),
    path("major-admin/", views.major_admin_dashboard, name="major_admin_dashboard"),
    path(
        "admin/review/<int:verification_id>/",
        views.admin_review_verification,
        name="admin_review_verification",
    ),
    path(
        "admin/profile/<int:profile_id>/",
        views.admin_edit_profile,
        name="admin_edit_profile",
    ),
    path(
        "admin/sections/",
        views.manage_sections,
        name="manage_sections",
    ),
    path(
        "admin/sections/create/",
        views.create_section,
        name="create_section",
    ),
    path("directory/", views.public_directory, name="public_directory"),
    path("profile/<str:username>/", views.public_profile_view, name="public_profile"),
    path("activity/", views.user_activity, name="user_activity"),
    path("checkout/", views.checkout_section, name="checkout_section"),
    path("checkout/create/", views.create_checkout, name="create_checkout"),
    path(
        "checkout/send/<int:transaction_id>/",
        views.send_mpesa_prompt,
        name="send_mpesa_prompt",
    ),
    path(
        "checkout/complete/<int:transaction_id>/",
        views.complete_transaction,
        name="complete_transaction",
    ),
]
