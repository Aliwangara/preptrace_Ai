from django.shortcuts import render,redirect
from .forms import SignupForm,LoginForm,ProfileForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from jobs.scraper import scrape_remotive,scrape_indeed
from jobs.models import Job
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse

# Create your views here.

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    form = LoginForm(request.POST or None)
    message = ''

    if request.method =="POST":
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email,password=password)

            if user is not None:
                login(request,user)
                return redirect('dashboard')
            else:
                message = 'Invalid email or password'
    return render(request, 'accounts/login.html', {'form': form, 'message': message})

def logout_view(request):
    logout(request)
    return redirect('login')
    
@login_required(login_url='login')
def dashboard_view(request):

    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return redirect('profile-setup')
    jobs = profile.jobs.all()

    query = request.GET.get("q","")
    site_filter = request.GET.get("site","")
    job_type_filter = request.GET.get("job_type","")

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(company__icontains=query) |
            Q(location__icontains=query)
        )

    if site_filter:
        jobs = jobs.filter(site__iexact=site_filter)
    
    if job_type_filter:
        jobs = jobs.filter(job_type__iexact=job_type_filter)

    for job in jobs:
        job.tech_list = [t.strip() for t in job.tech_stack.split(',')] if job.tech_stack else []

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('accounts/job_cards.html', {'jobs': jobs})
        return JsonResponse({'html': html})


    context = {
        "profile":profile,
        "jobs":jobs
    }

    
    return render(request,'accounts/dashboard.html', {'profile': profile, 'jobs': jobs})

@login_required(login_url='login')
def profile_setup_view(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None

    if request.method == "POST":
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            
            Job.objects.filter(profile=profile).delete()

            scraped_jobs = scrape_all(profile.role)
            print("SCRAPED JOBS:", scraped_jobs)

            for job in scraped_jobs:
                print("SAVING:", job["title"])
                Job.objects.create(
                    profile=profile,
                    title=job["title"],
                    company=job["company_name"],
                    location=job["candidate_required_location"],
                    link=job["url"],
                    site=job.get("site", "Remotive"),
                    logo=job.get("logo", ""),
                    tech_stack=','.join(job.get("tags", []))

                )
            return redirect('dashboard')

    else:
        form = ProfileForm(instance=profile)
    return render(request,'accounts/profile_setup.html',{'form': form})

def scrape_all(role):
    jobs = []

    # Remotive
    jobs += scrape_remotive(role)

    # Indeed
    jobs += scrape_indeed(role)

    # You can add more sources later easily
    return jobs







