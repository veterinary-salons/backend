from django.contrib import admin


@admin.register
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'first_name', 'last_name')
    search_fields = ('username',)
    list_filter = ('role',)
