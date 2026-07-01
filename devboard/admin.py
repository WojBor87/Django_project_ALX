from django.contrib import admin

from devboard.badges import render_status_badge

from .models import Project, Task, Comment

admin.site.register(Comment)

class TaskInline(admin.TabularInline):
    """Zadania wyświetlane wewnątrz projektu."""
    model = Task
    fields = ("title", "status", "priority", "assignee", "due_date")
    extra = 1
    show_change_link = True

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "owner",
        "created_at",
        "task_count"
    )
    search_fields = ("name", "description")
    list_filter = ("name","created_at")
    inlines = [TaskInline]

    @admin.display(description="Zadań")
    def task_count(self, obj):
        return obj.tasks.count()


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title", "project", "priority",
        "assignee", "due_date","status_badge_admin"
    )
    list_filter = ("status", "priority", "project", "assignee")
    search_fields = ("title", "description")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "description", "project")}),
        ("Przypisanie", {"fields": ("assignee", "due_date")}),
        ("Status", {"fields": ("status", "priority")}),
        ("Metadane", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    @admin.display(description="Status")
    def status_badge_admin(self, obj):
        return render_status_badge(obj)

admin.site.site_header = "DevBoard — Panel Administracyjny"
admin.site.site_title = "DevBoard Admin"
admin.site.index_title = "Zarządzanie projektem"