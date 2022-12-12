from django.contrib import admin

from lab.models import Chemical, Development, Step, Brand
from user.models import User


@admin.register(Chemical)
class ChemicalAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "type")
    list_display = (
        "name",
        "type",
        "brand",
    )
    list_filter = (
        "type",
    )
    ordering = ("brand__name", "type", "name")


class StepInline(admin.StackedInline):
    model = Step
    ordering = ("order",)
    show_change_link = False
    extra = 0


@admin.register(Development)
class DevelopmentAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "type")
    list_display = (
        "name",
        "type",
    )
    list_filter = (
        "type",
    )
    ordering = ("type", "name")
    inlines = (StepInline,)


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "development__type", "chemical__type")
    list_display = (
        "name",
        "development",
        "chemical",
        "order",
        "temperature",
        "accuracy",
        "duration",
    )
    list_filter = (
        "temperature",
    )
    ordering = ("development__type", "development__name", "order")


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    search_fields = ("id", "name")
    list_display = (
        "name",
    )
    ordering = ("name",)
