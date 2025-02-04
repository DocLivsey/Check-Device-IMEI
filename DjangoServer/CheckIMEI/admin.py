from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib import admin


def block_users(modeladmin, request, queryset):
    for user in queryset:
        user.is_active = False
        user.save()
        

block_users.short_description = 'Block selected users'


def unblock_users(modeladmin, request, queryset):
    for user in queryset:
        user.is_active = True
        user.save()
        

unblock_users.short_description = 'Unblock selected users'


class UserAdminForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    form = UserAdminForm

    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ['username', 'first_name', 'last_name']
    list_filter = ['is_staff', 'is_active']
    actions = [block_users, unblock_users]
