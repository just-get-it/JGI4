from django.db import models
from userdetail.models import *

# Create your models here.
class user_wallet(models.Model):
    user = models.ForeignKey(detail, on_delete=models.CASCADE)
    amount = models.FloatField(null=True, default=0.0)
    blockedAmount = models.FloatField(null=True,default=0.0)
    def __str__(self):
        return str(self.user.name)+" WALLET - Rs. "+str(self.amount)

    def get_transactions(self):
        res = []
        qs = self.wallet_transaction_set.all()
        for i in qs:
            res.append(i)
        return res

types = (
    ('Add', 'ADD'),
    ('Deduct', 'DEDUCT'),
    ('Block', 'BLOCK'),
)


class wallet_transaction(models.Model):
    wallet = models.ForeignKey(user_wallet, on_delete=models.DO_NOTHING)
    transactionType = models.CharField(max_length=25,choices=types,default='ADD') 
    payment_method = models.CharField(blank=True,max_length=256) 
    transaction_amount = models.FloatField(default=0.0)
    receiving_user = models.ForeignKey(detail, on_delete=models.DO_NOTHING, null=True)
    transaction_status = models.CharField(default="PENDING",max_length=256)
    is_successful = models.BooleanField(default=False) 
    razorpay_payment_id = models.CharField(max_length=256, null=True)
    razorpay_order_id = models.CharField(max_length=256, null=True)

    def __str__(self):
        return self.transactionType+" - "+str(self.transaction_amount)