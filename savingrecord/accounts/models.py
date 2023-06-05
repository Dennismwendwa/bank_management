from django.db import models
from django .contrib.auth.models import User
from PIL import Image
import os


# Create your models here.
class Profile(models.Model):
	user             = models.OneToOneField(User, on_delete=models.CASCADE)
	image            = models.ImageField(default="default.jpg", upload_to="profile_pics")
	about            = models.TextField()
	company          = models.CharField(max_length=100, blank=True, null=True)
	job              = models.CharField(max_length=100, blank=True, null=True)
	country          = models.CharField(max_length=100, blank=True, null=True)
	address          = models.CharField(max_length=100, blank=True, null=True)
	phone            = models.CharField(max_length=100, blank=True, null=True)
	twitter_profile  = models.CharField(max_length=100, blank=True, null=True)
	facebook_profile = models.CharField(max_length=100, blank=True, null=True)
	instagram_profile = models.CharField(max_length=100, blank=True, null=True)
	linkedin_profile = models.CharField(max_length=100, blank=True, null=True)

	def __str__(self):
		return f"{self.user.username} Profile"
	
	def save(self):
		#removing old pics after profile updates pics with new
		try:
			old_profile = Profile.objects.get(pk=self.pk)
		except Profile.DoesNotExist:
			old_profile = None

		if old_profile and self.image != old_profile.image:
			old_image_path = old_profile.image.path
			if os.path.exists(old_image_path):
				os.remove(old_image_path)

		super().save()

		#resizing images if bigger than 300 by 300
		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)
