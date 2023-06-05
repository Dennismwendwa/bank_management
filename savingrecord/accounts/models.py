from django.db import models
from django .contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
	user             = models.OneToOneField(User, on_delete=models.CASCADE)
	image            = models.ImageField(default="default.jpg", upload_to="profile_pics")
	about            = models.TextField()
	company          = models.CharField(max_length=100, blank=True, null=True)
	address          = models.CharField(max_length=100, blank=True, null=True)
	phone            = models.CharField(max_length=100, blank=True, null=True)
	twitter_profile  = models.CharField(max_length=100, blank=True, null=True)
	facebook_profile = models.CharField(max_length=100, blank=True, null=True)
	instagram_profile = models.CharField(max_length=100, blank=True, null=True)
	linkedin_profile = models.CharField(max_length=100, blank=True, null=True)

	def __str__(self):
		return f"{self.user.username} Profile"
