from accounts.models import JobApplication
from jobs.models import Job
from .cv_parser import extract_text_from_cv

def auto_apply_jobs(user, cv_path):
    profile = user.profile
    if profile.ats_score < 85:
        return []

    applied_jobs = []

    cv_text = extract_text_from_cv(cv_path).lower()
    jobs = Job.objects.filter(user=user)

    for job in jobs:
        # Combine job info for matching
        job_text = f"{job.title} {job.company} {job.location} {job.tech_stack}".lower()

        # Calculate % match
        match_count = sum(1 for word in job_text.split() if word in cv_text)
        total_words = len(job_text.split())
        match_percentage = (match_count / total_words) * 100 if total_words else 0

        # Auto-apply if match >= 80%
        if match_percentage >= 80:
            application, created = JobApplication.objects.get_or_create(
                user=user,
                job=job,
                defaults={"status": "applied"}
            )
            if created:
                applied_jobs.append(job.title)

    return applied_jobs
