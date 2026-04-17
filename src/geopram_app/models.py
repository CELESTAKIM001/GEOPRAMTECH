from django.db import models
from django.contrib.auth.models import User


class PageSection(models.Model):
    SECTION_CHOICES = [
        ("home_hero", "Home - Hero Section"),
        ("home_services", "Home - Services Section"),
        ("home_stats", "Home - Stats Section"),
        ("home_software", "Home - Software Section"),
        ("home_testimonials", "Home - Testimonials Section"),
        ("home_cta", "Home - CTA Section"),
        ("footer", "Footer"),
    ]
    page = models.CharField(max_length=50, choices=SECTION_CHOICES)
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("page",)

    def __str__(self):
        return f"{self.page} - {self.title}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TrainingEnrollment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    course = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.course}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(max_length=500, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    is_public = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    referral_code = models.CharField(max_length=20, unique=True, blank=True)
    referred_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="referrals",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    last_active = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_status(self):
        from django.utils import timezone
        from datetime import timedelta

        now = timezone.now()
        if self.last_active:
            diff = now - self.last_active
            if diff.total_seconds() < 300:
                return "active_now"
            elif diff.days < 1:
                return "active_today"
            elif diff.days < 7:
                return f"active_{diff.days}_days_ago"
            else:
                return f"active_{diff.days}_days_ago"
        return "inactive"


class UserSkill(models.Model):
    SKILL_CATEGORIES = [
        ("technical", "Technical"),
        ("design", "Design"),
        ("programming", "Programming"),
        ("gis", "GIS"),
        ("data", "Data Analysis"),
        ("other", "Other"),
    ]
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="skills"
    )
    name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=20, choices=SKILL_CATEGORIES, default="technical"
    )
    description = models.TextField(max_length=300, blank=True)
    is_verified = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.user.username} - {self.name}"


class UserItem(models.Model):
    ITEM_TYPES = [
        ("project", "Project"),
        ("portfolio", "Portfolio Item"),
        ("certification", "Certification"),
        ("service", "Service"),
        ("other", "Other"),
    ]
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="items"
    )
    title = models.CharField(max_length=200)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES, default="project")
    description = models.TextField(max_length=500, blank=True)
    link = models.URLField(blank=True)
    is_verified = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.user.username} - {self.title}"


class VerificationRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="verification_requests"
    )
    item_type = models.CharField(max_length=20)
    item_id = models.IntegerField()
    item_title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    admin_notes = models.TextField(blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_requests",
    )

    def __str__(self):
        return f"Verification: {self.item_title} - {self.status}"


class PublicProfile(models.Model):
    user = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="public_profile"
    )
    display_name = models.CharField(max_length=100)
    headline = models.CharField(max_length=200, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    verified_skills = models.ManyToManyField(
        UserSkill, related_name="public_profiles", blank=True
    )
    verified_items = models.ManyToManyField(
        UserItem, related_name="public_profiles", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name


class UserActivity(models.Model):
    ACTIVITY_TYPES = [
        ("login", "Login"),
        ("logout", "Logout"),
        ("profile_view", "Profile View"),
        ("directory_view", "Directory View"),
        ("page_visit", "Page Visit"),
        ("verification_request", "Verification Request"),
        ("skill_add", "Skill Added"),
        ("item_add", "Item Added"),
        ("profile_update", "Profile Update"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activities")
    activity_type = models.CharField(max_length=30, choices=ACTIVITY_TYPES)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.created_at}"


class SiteVisit(models.Model):
    visit_count = models.IntegerField(default=0)
    last_visit = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Site Visits"

    def __str__(self):
        return f"Visits: {self.visit_count}"


class CheckoutTransaction(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("initiated", "Initiated"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)
    service_name = models.CharField(max_length=200)
    service_description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    mpesa_receipt = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_transactions",
    )

    def __str__(self):
        return f"{self.customer_name} - {self.amount} - {self.status}"
