from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class DefaultAccountAdapterCustom(DefaultAccountAdapter):
    
    def send_mail(self, template_prefix, email, context):
        # print(context)
        try:
            # context['activate_url'] = settings.LOGIN_URL_FRONT + 'account-confirm-email/' + context['key']
            context['activate_url'] = settings.LOGIN_URL_FRONT + 'account-email-confirm/' + context['key'] + '/'
            msg = self.render_mail(template_prefix, email, context)
            msg.send()
        except:          
            url = context['password_reset_url']
            url = url.split('/')
            context['password_reset_url'] = settings.RESET_PASSWORD_URL_FRONT + \
                'password-reset-confirm/' + url[5]  + \
                '/' + url[6]
            msg = self.render_mail(template_prefix, email, context)
            msg.send()
            
            