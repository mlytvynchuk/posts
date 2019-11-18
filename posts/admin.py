from django.contrib import admin
from .models import Post,Comment
# Register your models here

class PostCommentInline(admin.TabularInline):
    model = Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','author', 'is_active')
    list_filter = ('is_active','date_posted')
    inlines = (PostCommentInline,)
    

admin.site.register(Comment)