from django.views.generic import TemplateView, CreateView, UpdateView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Contact, Profile
from .forms import ContactForm, LoginForm, CombinedProfileForm


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'mainapp/login.html'
    redirect_authenticated_user = True  # Redirects users who are already logged in
    extra_context = {'background_style': 'otherBody',
                     'viewname': 'login'}


class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = "mainapp/protected.html"
    extra_context = {'background_style': 'otherBody',
                     'viewname': 'protected'}
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        context['profile'] = self.request.user.profile
        return context


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mainapp/profile-detail.html'
    context_object_name = 'profile'
    extra_context = {'background_style': 'otherBody',
                     'viewname': 'profile-detail'}

    def get_object(self):
        return self.request.user.profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = CombinedProfileForm  # Use combined form
    template_name = 'mainapp/profile-update.html'
    success_url = reverse_lazy('profile-detail')
    extra_context = {
        'background_style': 'otherBody',
        'viewname': 'profile-update'
    }

    def get_object(self):
        return self.request.user.profile  # Get the current user's profile


class IndexView(TemplateView):
    template_name = "mainapp/index.html"
    extra_context = {'background_style': 'indexBody',
                     'viewname': 'index'}


class ContactFormCreateView(CreateView):
    form_class = ContactForm
    template_name = 'mainapp/contact.html'
    success_url = '/sent/'
    extra_context = {'background_style': 'otherBody',
                     'viewname': 'contact'}


class SentView(TemplateView):
    template_name = "mainapp/message_sent.html"
    sent = Contact.objects.all()
    extra_context = {'background_style': 'otherBody',
                     'sent': sent,
                     'viewname': 'sent'}
