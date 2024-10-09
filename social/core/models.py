from enum import Enum

from django.db import models


class User(models.Model):
    username = models.CharField(
        'Пользователь',
        max_length=255,
        blank=False
    )
    email = models.EmailField(
        'email',
        max_length=254,
        unique=True,
        blank=False
    )
    created_at = models.DateTimeField(
        'Дата регистрации',
        auto_now_add=True
    )
    avatar = models.ImageField(
        'Аватар пользователя',
        upload_to='users/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile'
    )
    bio = models.TextField(
        'О себе',
        blank=True
    )
    website = models.URLField(
        'Веб-сайт',
        blank=True
    )
    location = models.CharField(
        'Местоположение',
        max_length=50,
        blank=True
    )

    def __str__(self):
        return f'Профиль пользователя "{self.user.username}"'


class GroupType(Enum):
    PUBLIC = 'public'
    PRIVATE = 'private'


GROUP_TYPE_CHOICES = [(type.name, type.value) for type in GroupType]


class Group(models.Model):
    name = models.CharField(
        'Группа',
        max_length=255,
        blank=False
    )
    group_type = models.CharField(
        'Тип группы',
        max_length=20,
        choices=GROUP_TYPE_CHOICES,
        default=GroupType.PUBLIC.name
    )
    description = models.CharField(
        'Описание группы',
        max_length=255,
        blank=True
    )
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    owner = models.ForeignKey(
        User,
        related_name='groups',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Владелец'
    )

    class Meta:
        ordering = ['name']
        unique_together = ['name', 'description']

    def get_member_count(self):
        return self.subscribes.count()
    get_member_count.short_description = 'Количество подписчиков'

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(
        User,
        related_name='posts',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Автор'
    )
    text = models.TextField('Содержимое поста')
    image = models.ImageField(
        upload_to='posts/',
        blank=True
    )
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        'Дата изменения',
        auto_now=True
    )
    group = models.ForeignKey(
        Group,
        related_name='posts',
        on_delete=models.CASCADE,
        verbose_name='Группа'
    )

    class Meta:
        ordering = ['-created_at']

    def get_comments_count(self):
        return self.comments.count()
    get_comments_count.short_description = 'Количество комментариев'

    def __str__(self):
        return (self.text)


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE,
    )
    content = models.TextField('Комментарий')
    created_at = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-post']

    def __str__(self):
        return (
            f'Комментарий пользователя {self.author.username}. '
            f'Опубликован в ({self.created_at.date()})'
        )


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        related_name='subscribes',
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        Group,
        related_name='subscribes',
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ['user', 'group']

    def __str__(self):
        return f"{self.user.username} подписан на группу {self.group.name}"
