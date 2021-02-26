from django.db import models

#for the stripe api keys
class stripe_keys(models.Model):
    api_key = models.CharField(max_length=500,null=True, blank=True)
    endpoint_secret = models.CharField(max_length=500,null=True, blank=True)
    class Meta:
        verbose_name = 'Stripe Key'
        verbose_name_plural = 'Stripe Keys'
    # TO STRING METHOD
    def __str__(self):
        return self.api_key

#used in stripe success_url
class payment_tokens(models.Model):
    payment_token = models.CharField(max_length=500,null=True, blank=True)
    job = models.ForeignKey('services.Job', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Payment Token'
        verbose_name_plural = 'Payment Tokens'
    # TO STRING METHOD
    def __str__(self):
        return self.payment_token


        

        