# referrals/models.py
from django.db import models
from django.contrib.auth.models import User
from .utils import generate_referral_code

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    referral_code = models.CharField(max_length=12, blank=True)
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="recommended_by")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    def get_recommended_profiles(self):
        qs = Profile.objects.all()
        #my_recommended_profiles = [p for p in qs if p.recommended_by == self.user]
        my_recommended_profiles = []
        for profile in qs:
            if profile.recommended_by == self.user:
                my_recommended_profiles.append(profile)        
        return my_recommended_profiles
    
    def save(self, *args, **kwargs):
        if self.referral_code == "":
            referral_code = generate_referral_code()
            self.referral_code = referral_code
        super().save(*args, **kwargs)




