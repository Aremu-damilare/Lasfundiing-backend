from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from store.models import Order, Transaction, AccountType
from django.shortcuts import render




def Home(request):    
    account_type = AccountType.objects.all()
    features_list = account_type   
    return render(request, 'index.html', {'features_list': features_list})    



@method_decorator(login_required, name='dispatch')
class Dashboard(TemplateView):
    template_name = "dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['email'] = user.email
        context['firstname'] = user.first_name
        context['lastname'] = user.last_name
        
        # Check if user has any paid order
        has_paid_order = Order.objects.filter(user=user, paid=True).exists()
        context['has_paid_order'] = has_paid_order
        context['transactions'] = Transaction.objects.filter(user=self.request.user).order_by('-created_at')[:3]
        print(has_paid_order,  context['has_paid_order'])
        return context
    
    
    
