from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # This save method belongs to the Profile model
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

# These are signal receivers (separate from the model's save method)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()  # This calls the Profile's save() method


class Contact(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name')
    email = models.EmailField(verbose_name='E-Mail')
    phone = models.CharField(max_length=15, verbose_name='Phone')
    subject = models.CharField(max_length=255, verbose_name='Subject')
    message = models.TextField(verbose_name='Message')
    when_sent = models.DateTimeField(default=now, editable=False)
    replied = models.BooleanField(default=False)
    when_replied = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
