from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.generic import TemplateView

# Create your views here.
class IndexView(TemplateView):
    template_name = "accounting/index.html"

class AccountsView(TemplateView):
    template_name = "accounting/accounts.html"
