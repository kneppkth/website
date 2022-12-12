from django.contrib import admin

from user.models import User, Membership


class MembershipInline(admin.StackedInline):
    model = Membership
    ordering = ("-date_from", "-date_to")
    show_change_link = False
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ("id", "email", "firstname", "lastname")
    list_display = (
        "email",
        "firstname",
        "lastname",
        "email_verified",
        "registration_finished",
        "is_active",
        "created_at",
    )
    list_filter = (
        "email_verified",
        "registration_finished",
        "is_active",
        "gender",
        "university",
        "degree",
        "graduation_year",
    )
    readonly_fields = (
        "groups",
        "last_login",
        "created_at",
    )
    exclude = ("password", "user_permissions")
    ordering = ("-created_at",)
    inlines = (MembershipInline,)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    search_fields = ("id", "user")
    list_display = (
        "user",
        "type",
        "is_paid",
        "date_from",
        "date_to",
    )
    list_filter = (
        "type",
        "is_paid",
        "date_from",
        "date_to",
    )
    ordering = ("-date_from", "-date_to")
