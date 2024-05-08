"""Admin configuration."""

from django.contrib import admin

from will_of_the_prophets import models

admin.site.register(models.Butthole)
admin.site.register(models.SpecialSquareType)


@admin.register(models.Roll)
class PersonAdmin(admin.ModelAdmin):  # noqa: D101
    list_display = ("number", "embargo", "created", "modified")
    list_display_links = list_display
    ordering = ("-embargo",)


@admin.register(models.SpecialSquare)
class SpecialSquareAdmin(admin.ModelAdmin):  # noqa: D101
    list_display = ("type", "square", "start", "end")
    list_display_links = list_display
    ordering = ("square",)
