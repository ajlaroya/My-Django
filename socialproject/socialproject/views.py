from django.conf import settings
from django.views.generic import TemplateView
from django.shortcuts import render
from django.core.mail import send_mail
from accounts.forms import ContactForm

class HomePage(TemplateView):
    template_name = 'index.html'

class AboutPage(TemplateView):
    template_name = 'about.html'

class ContactPage(TemplateView):
    template_name = 'contact.html'

    def get(self,request):
        form = ContactForm()
        context = {'form': form}
        return render(request, 'contact.html', context)

    def post(self,request):
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                form.save()
                email_subject = f'Plume Contact | {form.cleaned_data["email"]}: {form.cleaned_data["subject"]}'
                email_message = form.cleaned_data['message']
                send_mail(email_subject, email_message, settings.CONTACT_EMAIL, settings.ADMIN_EMAIL, fail_silently=False,)
                return render(request, 'success.html')
