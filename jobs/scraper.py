# import requests
# from bs4 import BeautifulSoup

# def scrape_indeed(role):
#     role = role.replace(" ", "+")
#     url = f"https://www.indeed.com/jobs?q={role}&l="

#     headers = {
#         "User-Agent": "Mozilla/5.0"
#     }

#     response = requests.get(url, headers=headers)

#     if response.status_code != 200:
#         return []

#     soup = BeautifulSoup(response.text, "html.parser")

#     job_cards = soup.select("div.job_seen_beacon")

#     jobs = []

#     for card in job_cards[:10]:
#         title = card.select_one("h2.jobTitle")
#         company = card.select_one("span.companyName")
#         location = card.select_one("div.companyLocation")
#         link = card.select_one("a")

#         if not title or not company or not link:
#             continue

#         jobs.append({
#             "title": title.get_text(strip=True),
#             "company": company.get_text(strip=True),
#             "location": location.get_text(strip=True) if location else "Remote",
#             "link": "https://www.indeed.com" + link["href"],
#             "site": "Indeed"
#         })
#         print("STATUS:", response.status_code)
#         print(response.text[:1000])

#     return jobs


# jobs/scraper.py
import requests
from bs4 import BeautifulSoup

def scrape_remotive(role):
    """Scrape jobs from Remotive API for a given role."""
    url = "https://remotive.com/api/remote-jobs"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()
    jobs = []

    role = role.lower()

    for job in data.get("jobs", []):
        title = job.get("title", "").lower()
        if role in title or any(word in title for word in role.split()):
            jobs.append({
                "title": job.get("title", "No Title"),
                "company": job.get("company_name", "Unknown Company"),
                "location": job.get("candidate_required_location", "Worldwide"),
                "link": job.get("url", "#"),
                "site": "Remotive",                      # default site
                "logo": job.get("company_logo", ""),      # default empty
            })

    return jobs[:20]  

def scrape_indeed(role, location=""):
    """Scrape jobs from Indeed website for a given role."""
    headers = {"User-Agent": "Mozilla/5.0"}
    query = "+".join(role.split())
    url = f"https://www.indeed.com/jobs?q={query}&l={location}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    jobs = []

    for div in soup.find_all("div", class_="job_seen_beacon")[:20]:
        title_tag = div.find("h2")
        company_tag = div.find("span", class_="companyName")
        location_tag = div.find("div", class_="companyLocation")
        link_tag = title_tag.find("a") if title_tag else None

        if not title_tag or not company_tag or not link_tag:
            continue

        job_link = "https://www.indeed.com" + link_tag.get("href", "#")

        jobs.append({
            "title": title_tag.text.strip(),
            "company": company_tag.text.strip(),
            "location": location_tag.text.strip() if location_tag else "Unknown",
            "link": job_link,
            "site": "Indeed",
            "logo": ""  # Indeed does not provide logos
        })

    return jobs

