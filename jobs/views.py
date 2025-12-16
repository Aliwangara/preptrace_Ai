from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from .scraper import scrape_indeed

# Create your views here.

@login_required(login_url='login')
def dashboard(request):
