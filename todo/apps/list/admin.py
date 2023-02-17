from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin
# Register your models here.


@admin.register(models.TodoList)
class TodoListAdmin(admin.ModelAdmin):
    list_display = ["task", "completed"]

@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    list_display = ("email",'created', 'updated')
    ordering = ("email",)

    fieldsets = (
        (None, {'fields': ('email', 'password','first_name', 'last_name')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    list_filter = ('staff', 'admin', 'active', 'groups')
    search_fields = ('email', 'first_name', 'last_name', 'email')

# class MyModelAdmin(admin.ModelAdmin):
#     def save_model(self, request, obj, form, change):
#         if not obj.pk:
#             # Only set the password when the user is created
#             obj.password = make_password(form.cleaned_data['password'])
#         super().save_model(request, obj, form, change)
#
#
# admin.site.register(models.User, CustomUserAdmin)
