from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model

from Cosmetic_studio.accounts.forms import CreateUserForm, StudioUserChangeForm

UserModel = get_user_model()


@admin.register(UserModel)
class StudioUserAdmin(auth_admin.UserAdmin):
    model = UserModel
    add_form = CreateUserForm
    form = StudioUserChangeForm
    list_display = ['pk', 'email', 'user_name', 'is_staff', 'is_superuser', 'date_joined']
    search_fields = ['email']
    list_display_links = ('pk', 'email',)
    ordering = ['pk']
    readonly_fields = ('date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('user_name', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "user_name", "password1", "password2"),
            },
        ),
    )
