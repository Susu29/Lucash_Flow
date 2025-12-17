from .models import Accounts
from django.views.generic import TemplateView, ListView, DetailView

# Create your views here.
class IndexView(TemplateView):
    template_name = "accounting/index.html"

class AccountsView(ListView):
    template_name = "accounting/accounts.html"
    model = Accounts
    context_object_name = "Accounts"
