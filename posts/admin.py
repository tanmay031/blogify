# posts/admin.py

from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','content','created_at', 'updated_at')  # Columns to display in the list view
    search_fields = ('title', 'content')  # Search functionality

# Register the Post model with the customized admin class
admin.site.register(Post, PostAdmin)
