from django.contrib import admin

# Register your models here.
from .models import Notifications





class notificationsAdmin(admin.ModelAdmin):
    #add_form = budgetForm
    model = Notifications
    list_display = [
        "notification_ID",
        "notification_text",
        "notification_time",
        "notification_viewer",

    ]


admin.site.register(Notifications, notificationsAdmin)
