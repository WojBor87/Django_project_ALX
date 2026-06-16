from django.contrib import admin
from .models import Project, Task, Comment


class TaskInline(admin.TabularInline):
    model = Task
    fields = ("title", "status", "priority", "assignee", "due_date")
    extra = 1
    show_change_link = True

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('name',)
    ordering = ('-created_at', 'owner')

    inlines = [TaskInline]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assignee', 'status', 'priority', 'due_date')
    search_fields = ('title','assignee', 'status')
    list_filter = ('status',)

    empty_value_display = "--- empty ---"
    ordering = ('-due_date',)

    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "description", "project")}),
        ("Przypisanie", {"fields": ("assignee", "due_date")}),
        ("Status", {"fields": ("status", "priority")}),
        ("Metadane", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'author')
    search_fields = ('task', 'author')
