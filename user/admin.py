from django.contrib import admin
from django.contrib.auth.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username',)
    list_filter = ('is_staff', 'is_superuser')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.site_header = "DayJeong 관리자"
admin.site.site_title = "DayJeong Admin"
admin.site.index_title = "관리자 페이지"