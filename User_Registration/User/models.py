from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
from datetime import timedelta

# Create your models here.
class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=6, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)  # ✅ instead of auto_now_add
    resend_count = models.IntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)

    def generate_code(self):
        self.code = str(random.randint(100000, 999999))
        self.created_at = timezone.now()  # refresh on every OTP generation
        self.save()
        return self.code

    def is_expired(self):
        from datetime import timedelta
        return timezone.now() > self.created_at + timedelta(minutes=1)

    def is_locked(self):
        return self.locked_until and timezone.now() < self.locked_until

    def lock_for_2_hours(self):
        from datetime import timedelta
        self.locked_until = timezone.now() + timedelta(hours=2)
        self.save()

    def __str__(self):
        return f"{self.email} - {self.code}"