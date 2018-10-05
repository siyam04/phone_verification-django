from django.db import models

# Create your models here.

class PhoneRegistration(models.Model):
	phone_number = models.CharField(max_length=50, unique=True)
	otp_code = models.CharField(max_length=6)
	otp_passed = models.BooleanField(default=False)

	def __str__(self):
		return self.phone_number
