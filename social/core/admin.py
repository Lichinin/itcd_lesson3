from django.contrib import admin
from django.utils.html import format_html

from .models import Comment, Group, Post, Subscribe, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'avatar_preview', 'created_at')
    readonly_fields = ('avatar_preview',)

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;"/>'.format(obj.avatar.url))
        else:
            return 'No image'
    avatar_preview.short_description = 'Avatar Preview'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_member_count', 'group_type', 'description', 'owner', 'created_at')
    list_filter = ('owner',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('text', 'image', 'get_comments_count', 'group', 'author', 'created_at', 'updated_at')
    list_filter = ('author', 'group')
    search_fields = ('text__iregex',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'post', 'created_at')
    list_filter = ('post', 'author')


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', '__str__',)
    list_filter = ('user', 'group')
