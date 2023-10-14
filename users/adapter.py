from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist



class DefaultAccountAdapterCustom(DefaultAccountAdapter):    
    def render_mail(self, template_prefix, email, context, headers=None):
        """
        Renders an e-mail to `email`.  `template_prefix` identifies the
        e-mail that is to be sent, e.g. "account/email/email_confirmation"
        """
        to = [email] if isinstance(email, str) else email
        subject = render_to_string("{0}_subject.txt".format(template_prefix), context)
        # remove superfluous line breaks
        subject = " ".join(subject.splitlines()).strip()
        subject = self.format_email_subject(subject)

        from_email = self.get_from_email()

        bodies = {}
        for ext in ["html"]:
            try:
                template_name = "{0}_message.{1}".format(template_prefix, ext)
                bodies[ext] = render_to_string(
                    template_name,
                    context,
                    self.request,
                ).strip()
            except TemplateDoesNotExist:
                if ext == "txt" and not bodies:
                    # We need at least one body
                    raise
        if "txt" in bodies:
            msg = EmailMultiAlternatives(
                subject, bodies["txt"], from_email, to, headers=headers
            )
            if "html" in bodies:
                msg.attach_alternative(bodies["html"], "text/html")
        else:
            msg = EmailMessage(subject, bodies["html"], from_email, to, headers=headers)
            msg.content_subtype = "html"  # Main content is now text/html
        return msg
    
    def send_mail(self, template_prefix, email, context):
        # print("context \n", context)
        # print("template_prefix \n", template_prefix)
        # print("email \n", email)
        try:
            # context['activate_url'] = settings.LOGIN_URL_FRONT + 'account-confirm-email/' + context['key']
            context['activate_url'] = settings.BACKEND_URL + 'account-email-confirm/' + context['key'] + '/'
            msg = self.render_mail(template_prefix, email, context)
            msg.send()
        except:          
            url = context['password_reset_url']
            # ['http:', '', 'localhost:8000', 'password-reset-confirm', 'j', 'bvwume-d2a7641bcb9d8242f38d9cef15ee66aa', '']
            url = url.split('/')
            
            # url = url.split('/')
            # context['password_reset_url'] = settings.RESET_PASSWORD_URL_FRONT + 'password-reset-confirm/' + url[5]  + '/' + url[6]
            context['password_reset_url'] = settings.RESET_PASSWORD_URL_FRONT + '?uid=' + url[4]  + '&token=' + url[5]
            print(url)
            msg = self.render_mail(template_prefix, email, context)
            msg.send()