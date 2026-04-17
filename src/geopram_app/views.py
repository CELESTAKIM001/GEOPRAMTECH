from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from django.core.mail import send_mail
from datetime import timedelta
from .models import (
    UserProfile,
    UserSkill,
    UserItem,
    VerificationRequest,
    PublicProfile,
    UserActivity,
    SiteVisit,
    CheckoutTransaction,
)
from django.http import JsonResponse
from django.db.models import Count


def home(request):
    from django.db.models import F

    try:
        visit, _ = SiteVisit.objects.get_or_create(id=1)
        visit.visit_count = F("visit_count") + 1
        visit.save(update_fields=["visit_count"])
    except Exception:
        pass

    if request.user.is_authenticated:
        try:
            UserActivity.objects.create(
                user=request.user,
                activity_type="page_visit",
                description=f"Visited home page",
                ip_address=request.META.get("REMOTE_ADDR"),
            )
        except Exception:
            pass
    return render(request, "home.html")


def services(request):
    return render(request, "services.html")


def software(request):
    return render(request, "software.html")


def solutions(request):
    return render(request, "solutions.html")


def training(request):
    return render(request, "training.html")


def terms(request):
    return render(request, "terms.html")


@login_required
def dashboard(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        return redirect("profile_create")

    skills = profile.skills.all()
    items = profile.items.all()
    pending_verifications = VerificationRequest.objects.filter(
        user_profile=profile, status="pending"
    ).count()

    context = {
        "profile": profile,
        "skills": skills,
        "items": items,
        "pending_verifications": pending_verifications,
        "projects_count": 150,
        "clients_count": 45,
        "training_completed": 12,
        "referrals_count": profile.referrals.count(),
    }
    return render(request, "user_dashboard.html", context)


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            UserActivity.objects.create(
                user=user,
                activity_type="login",
                description=f"User logged in",
                ip_address=request.META.get("REMOTE_ADDR"),
            )
            messages.success(request, "Welcome to GEOPRAM Dashboard!")
            if user.is_staff:
                return redirect("major_admin_dashboard")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials")
    return render(request, "login.html")


def logout_view(request):
    if request.user.is_authenticated:
        UserActivity.objects.create(
            user=request.user,
            activity_type="logout",
            description=f"User logged out",
            ip_address=request.META.get("REMOTE_ADDR"),
        )
    logout(request)
    messages.info(request, "You have been logged out")
    return redirect("home")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        Contact.objects.create(name=name, email=email, phone=phone, message=message)

        subject = f"New Contact from {name} - GEOPRAM TECH"
        email_message = f"""
New contact form submission:

Name: {name}
Email: {email}
Phone: {phone}

Message:
{message}
"""
        try:
            send_mail(
                subject,
                email_message,
                "geopramtech@gmail.com",
                ["geopramtech@gmail.com"],
                fail_silently=False,
            )
            messages.success(
                request, "Thank you for contacting us! We will get back to you soon."
            )
        except Exception as e:
            messages.success(
                request, "Thank you for contacting us! We will get back to you soon."
            )
    return render(request, "contact.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        referral_code = request.POST.get("referral_code", "").strip()

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "register.html")

        referrer_profile = None
        if referral_code:
            referrer_profile = UserProfile.objects.filter(
                referral_code=referral_code
            ).first()
            if not referrer_profile:
                messages.warning(
                    request,
                    "Invalid referral code. Account will be created without referral points.",
                )

        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        profile = UserProfile.objects.create(user=user, referred_by=referrer_profile)

        if referrer_profile:
            referrer_profile.points += 100
            referrer_profile.save()
            messages.success(
                request,
                f"Account created! You used referral code from {referrer_profile.user.username}. They earned 100 points!",
            )

        login(request, user)
        messages.success(request, "Account created! Complete your profile.")
        return redirect("dashboard")

    return render(request, "register.html")


@login_required
def profile_create(request):
    try:
        if request.user.profile:
            return redirect("dashboard")
    except UserProfile.DoesNotExist:
        pass

    if request.method == "POST":
        profile = UserProfile.objects.create(
            user=request.user,
            bio=request.POST.get("bio", ""),
            phone=request.POST.get("phone", ""),
            location=request.POST.get("location", ""),
            company=request.POST.get("company", ""),
            website=request.POST.get("website", ""),
        )
        UserActivity.objects.create(
            user=request.user,
            activity_type="profile_update",
            description=f"Profile created",
            ip_address=request.META.get("REMOTE_ADDR"),
        )
        messages.success(
            request, "Profile created! Admin will review to make it public."
        )
        return redirect("dashboard")

    return render(request, "profile_create.html")


@login_required
def profile_edit(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        return redirect("profile_create")

    if request.method == "POST":
        profile.bio = request.POST.get("bio", profile.bio)
        profile.phone = request.POST.get("phone", profile.phone)
        profile.location = request.POST.get("location", profile.location)
        profile.company = request.POST.get("company", profile.company)
        profile.website = request.POST.get("website", profile.website)
        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("dashboard")

    return render(request, "profile_edit.html")


@login_required
def add_skill(request):
    if request.method == "POST":
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            return redirect("profile_create")

        skill = UserSkill.objects.create(
            user=profile,
            name=request.POST.get("name"),
            category=request.POST.get("category", "technical"),
            description=request.POST.get("description", ""),
        )
        messages.success(
            request, "Skill added! Request verification to make it visible publicly."
        )
        return redirect("dashboard")

    return render(request, "skill_form.html")


@login_required
def add_item(request):
    if request.method == "POST":
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            return redirect("profile_create")

        item = UserItem.objects.create(
            user=profile,
            title=request.POST.get("title"),
            item_type=request.POST.get("item_type", "project"),
            description=request.POST.get("description", ""),
            link=request.POST.get("link", ""),
        )
        messages.success(
            request, "Item added! Request verification to make it visible publicly."
        )
        return redirect("dashboard")

    return render(request, "item_form.html")


@login_required
def request_verification(request, item_type, item_id):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        return redirect("profile_create")

    if item_type == "skill":
        item = get_object_or_404(UserSkill, id=item_id, user=profile)
        item_title = item.name
    elif item_type == "item":
        item = get_object_or_404(UserItem, id=item_id, user=profile)
        item_title = item.title
    else:
        messages.error(request, "Invalid item type")
        return redirect("dashboard")

    if VerificationRequest.objects.filter(
        user_profile=profile, item_id=item_id, item_type=item_type, status="pending"
    ).exists():
        messages.error(request, "Verification already requested for this item")
        return redirect("dashboard")

    VerificationRequest.objects.create(
        user_profile=profile,
        item_type=item_type,
        item_id=item_id,
        item_title=item_title,
        status="pending",
    )
    messages.success(
        request, "Verification request submitted! Admin will review shortly."
    )
    return redirect("dashboard")


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect("dashboard")

    pending_verifications = VerificationRequest.objects.filter(
        status="pending"
    ).select_related("user_profile__user")
    all_profiles = UserProfile.objects.select_related("user").order_by("-created_at")
    verification_history = VerificationRequest.objects.exclude(
        status="pending"
    ).order_by("-reviewed_at")[:20]

    context = {
        "pending_verifications": pending_verifications,
        "all_profiles": all_profiles,
        "verification_history": verification_history,
    }
    return render(request, "admin_dashboard.html", context)


@login_required
def admin_review_verification(request, verification_id):
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect("dashboard")

    verification = get_object_or_404(VerificationRequest, id=verification_id)

    if request.method == "POST":
        action = request.POST.get("action")
        admin_notes = request.POST.get("admin_notes", "")

        if action == "approve":
            verification.status = "approved"
            verification.reviewed_by = request.user
            verification.reviewed_at = timezone.now()
            verification.admin_notes = admin_notes
            verification.save()

            if verification.item_type == "skill":
                skill = UserSkill.objects.get(id=verification.item_id)
                skill.is_verified = True
                skill.is_public = True
                skill.save()
            elif verification.item_type == "item":
                item = UserItem.objects.get(id=verification.item_id)
                item.is_verified = True
                item.is_public = True
                item.save()

            messages.success(request, f"Verified: {verification.item_title}")
        elif action == "reject":
            verification.status = "rejected"
            verification.reviewed_by = request.user
            verification.reviewed_at = timezone.now()
            verification.admin_notes = admin_notes
            verification.save()
            messages.info(request, f"Rejected: {verification.item_title}")

        return redirect("admin_dashboard")

    context = {
        "verification": verification,
    }
    return render(request, "admin_review.html", context)


@login_required
def admin_edit_profile(request, profile_id):
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect("dashboard")

    profile = get_object_or_404(UserProfile, id=profile_id)

    if request.method == "POST":
        profile.is_public = request.POST.get("is_public") == "on"
        profile.bio = request.POST.get("bio", profile.bio)
        profile.phone = request.POST.get("phone", profile.phone)
        profile.location = request.POST.get("location", profile.location)
        profile.company = request.POST.get("company", profile.company)
        profile.website = request.POST.get("website", profile.website)
        profile.save()
        messages.success(request, f"Profile updated for {profile.user.username}")
        return redirect("admin_dashboard")

    context = {
        "profile": profile,
    }
    return render(request, "admin_profile_edit.html", context)


@login_required
def admin_delete_profile(request, profile_id):
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect("dashboard")

    profile = get_object_or_404(UserProfile, id=profile_id)
    username = profile.user.username

    profile.user.delete()
    profile.delete()

    messages.success(request, f"User '{username}' has been deleted successfully.")
    return redirect("admin_dashboard")


@login_required
def public_directory(request):
    public_profiles = UserProfile.objects.filter(is_public=True).select_related("user")

    query = request.GET.get("q", "")
    if query:
        public_profiles = public_profiles.filter(
            models.Q(user__username__icontains=query)
            | models.Q(bio__icontains=query)
            | models.Q(company__icontains=query)
        )

    context = {
        "public_profiles": public_profiles,
        "query": query,
    }
    return render(request, "public_directory.html", context)


def public_profile_view(request, username):
    profile = get_object_or_404(UserProfile, user__username=username, is_public=True)
    verified_skills = profile.skills.filter(is_verified=True, is_public=True)
    verified_items = profile.items.filter(is_verified=True, is_public=True)

    context = {
        "profile": profile,
        "verified_skills": verified_skills,
        "verified_items": verified_items,
    }
    return render(request, "public_profile.html", context)


@login_required
def user_activity(request):
    profile = request.user.profile
    profile.last_active = timezone.now()
    profile.save()
    return redirect("dashboard")


@login_required
def manage_sections(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect("dashboard")

    from .models import PageSection

    if request.method == "POST":
        section_id = request.POST.get("section_id")
        section = get_object_or_404(PageSection, id=section_id)
        section.title = request.POST.get("title", section.title)
        section.content = request.POST.get("content", section.content)
        section.is_active = request.POST.get("is_active") == "on"
        section.save()
        messages.success(
            request, f"Section '{section.get_page_display()}' updated successfully!"
        )
        return redirect("manage_sections")

    sections = PageSection.objects.all()
    return render(request, "manage_sections.html", {"sections": sections})


@login_required
def create_section(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect("dashboard")

    from .models import PageSection

    if request.method == "POST":
        page = request.POST.get("page")
        title = request.POST.get("title")
        content = request.POST.get("content")

        section, created = PageSection.objects.update_or_create(
            page=page, defaults={"title": title, "content": content, "is_active": True}
        )
        messages.success(
            request,
            f"Section '{section.get_page_display()}' created/updated successfully!",
        )
        return redirect("manage_sections")

    return redirect("manage_sections")


@login_required
def major_admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect("dashboard")

    pending_verifications = VerificationRequest.objects.filter(
        status="pending"
    ).select_related("user_profile__user")
    all_profiles = UserProfile.objects.select_related("user").order_by("-created_at")
    verification_history = VerificationRequest.objects.exclude(
        status="pending"
    ).order_by("-reviewed_at")[:20]

    login_activities = (
        UserActivity.objects.filter(activity_type__in=["login", "logout"])
        .select_related("user")
        .order_by("-created_at")[:50]
    )

    all_activities = UserActivity.objects.select_related("user").order_by(
        "-created_at"
    )[:100]

    best_referrers = (
        UserProfile.objects.annotate(referral_count=Count("referrals"))
        .filter(referral_count__gt=0)
        .order_by("-referral_count")[:5]
    )

    try:
        site_visit = SiteVisit.objects.get(id=1)
        total_visits = site_visit.visit_count
    except SiteVisit.DoesNotExist:
        total_visits = 0

    stk_transactions = CheckoutTransaction.objects.all().order_by("-created_at")[:20]

    context = {
        "pending_verifications": pending_verifications,
        "all_profiles": all_profiles,
        "verification_history": verification_history,
        "login_activities": login_activities,
        "all_activities": all_activities,
        "best_referrers": best_referrers,
        "total_visits": total_visits,
        "stk_transactions": stk_transactions,
    }
    return render(request, "major_admin_dashboard.html", context)


@login_required
def checkout_section(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect("dashboard")

    transactions = CheckoutTransaction.objects.order_by("-created_at")
    context = {"transactions": transactions}
    return render(request, "checkout_section.html", context)


@login_required
def create_checkout(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect("dashboard")

    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        customer_phone = request.POST.get("customer_phone")
        service_name = request.POST.get("service_name")
        service_description = request.POST.get("service_description")
        amount = request.POST.get("amount")

        transaction = CheckoutTransaction.objects.create(
            customer_name=customer_name,
            customer_phone=customer_phone,
            service_name=service_name,
            service_description=service_description,
            amount=amount,
            status="pending",
            created_by=request.user,
        )
        messages.success(
            request, f"Checkout created for {customer_name}. Prompt will be sent."
        )
        return redirect("checkout_section")

    return redirect("checkout_section")


@login_required
def send_mpesa_prompt(request, transaction_id):
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect("dashboard")

    try:
        transaction = CheckoutTransaction.objects.get(id=transaction_id)
        transaction.status = "initiated"
        transaction.save()
        messages.success(request, f"MPESA prompt sent to {transaction.customer_phone}")
    except CheckoutTransaction.DoesNotExist:
        messages.error(request, "Transaction not found")

    return redirect("checkout_section")


@login_required
def complete_transaction(request, transaction_id):
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admin only.")
        return redirect("dashboard")

    try:
        transaction = CheckoutTransaction.objects.get(id=transaction_id)
        if request.method == "POST":
            receipt = request.POST.get("mpesa_receipt", "")
            transaction.mpesa_receipt = receipt
            transaction.status = "completed"
            transaction.save()
            messages.success(
                request, f"Transaction {transaction_id} marked as completed"
            )
        else:
            transaction.status = "completed"
            transaction.save()
            messages.success(
                request, f"Transaction {transaction_id} marked as completed"
            )
    except CheckoutTransaction.DoesNotExist:
        messages.error(request, "Transaction not found")

    return redirect("checkout_section")
