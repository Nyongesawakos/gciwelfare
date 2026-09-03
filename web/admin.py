from django.contrib import admin

# Register your models here.
from .models import BulkMessage, user, tips,room, message,group, update,cash_expenditure,Msg, MpesaTransaction,OpeningBalance, BulkMessage
admin.site.register(user)
admin.site.register(tips)
admin.site.register(room)
admin.site.register(message)
admin.site.register(group)
admin.site.register(Msg)
admin.site.register(update)
admin.site.register(cash_expenditure)
admin.site.register(MpesaTransaction)
admin.site.register(OpeningBalance)
admin.site.register(BulkMessage)
from .models import WhatsAppContact

@admin.register(WhatsAppContact)
class WhatsAppContactAdmin(admin.ModelAdmin):
    list_display = ("name", "phone")




