from django import forms
from django.core.mail import EmailMessage
from django.db import transaction
from decouple import config
from .models import Contact, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


class CombinedProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        required=False,
        label="First Name",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        label="Last Name",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )

    # Profile model fields (handled via Meta)
    class Meta:
        model = Profile
        fields = ['image']  # Only specify Profile fields here

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prefill User data if available
        if hasattr(self.instance, 'user') and self.instance.user:
            user = self.instance.user
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def clean_email(self):
        """Validate email uniqueness (excluding current user)."""
        email = self.cleaned_data.get('email')
        if hasattr(self.instance, 'user') and self.instance.user:
            if User.objects.exclude(pk=self.instance.user.pk).filter(email=email).exists():
                raise forms.ValidationError("This email is already in use.")
        return email

    def clean_image(self):
        """Validate image size (max 32MB)."""
        image = self.cleaned_data.get('image')
        if image and image.size > 32 * 1024 * 1024:  # 32MB
            raise forms.ValidationError("Image file too large ( > 32MB )")
        return image

    def save(self, commit=True):
        """Save both User and Profile data."""
        profile = super().save(commit=False)
        
        # Handle the image file separately
        if 'image' in self.changed_data:
            profile.image = self.cleaned_data['image']
        
        if hasattr(self.instance, 'user') and self.instance.user:
            user = self.instance.user
            # Update User fields
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
        
        if commit:
            profile.save()
            self.save_m2m()  # In case you add many-to-many fields later
        
        return profile

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'phone', 'subject', 'message')
        exclude = ('when_sent', 'replied', 'when_replied')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def save(self):
        instance = super(ContactForm, self).save()

        @transaction.on_commit
        def contact_sendemail():
            email = EmailMessage(
                f"From: {instance.email} -> {instance.subject}",
                f"({instance.email}) -> {instance.message}",
                config("EMAIL_HOST_USER"),
                [config("EMAIL_HOST_USER")],
                reply_to=[instance.email],
            )
            email.send(fail_silently=True)
        return instance
