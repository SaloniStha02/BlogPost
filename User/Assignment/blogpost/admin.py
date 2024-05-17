from django.contrib import admin
from .models import BlogPost

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_date', 'description']
    fieldsets = (
        (None, {'fields': ('title', 'description')}),
        ('Permissions', {'fields': ('is_deleted',)}),
    )

admin.site.register(BlogPost, BlogPostAdmin)