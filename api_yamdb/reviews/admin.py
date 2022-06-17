from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User

models = (Category, Comment, Genre, Review, Title,)

for model in models:
    admin.site.register(model)


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'bio', 'role'
    )
    list_filter = ('username',)
    search_fields = ('username', 'role')
    fields = (
        'username', 'email', 'first_name', 'last_name', 'bio', 'role'
    )
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
