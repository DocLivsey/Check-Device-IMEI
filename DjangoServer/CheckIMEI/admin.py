from django.forms import ModelForm
from django.contrib import admin
from django.contrib.auth.users import User


def block_user(user: User):
    user.is_active = False
    user.save()
    

def block_users(modeladmin, request, queryset):
    for user in queryset:
        block_user(user)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name')
    ordering = ('username',)
    list_filter = ('is_staff', 'is_active')
    actions = [block_users]
    
    
class UserAdminForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
