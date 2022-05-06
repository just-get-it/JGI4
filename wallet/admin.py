from django.contrib import admin
from .models import *
# Register your models here.

class user_walletAdmin(admin.ModelAdmin):
	list_display=['__str__','get_transactions']

class wallet_transactionAdmin(admin.ModelAdmin):
	list_display=['__str__','wallet']

admin.site.register(user_wallet,user_walletAdmin)
admin.site.register(wallet_transaction,wallet_transactionAdmin)