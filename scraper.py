
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import requests
import csv

keywords = ["intern", "internship", "graduate", "placement"]
urls = [
    "https://www.linkedin.com/jobs/search/?keywords=intern",
    "https://careers.google.com/jobs/results/",
    "https://www.amazon.jobs/en/jobs"
]

def is_relevant(title):
    return any(k.lower() in title.lower() for k in keywords)

def scrape_linkedin(driver):
    driver.get(urls[0])
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    jobs = soup.find_all("a", {"class": "base-card__full-link"})
    results = []
    for job in jobs:
        title = job.text.strip()
        if is_relevant(title):
            results.append(("LinkedIn", title, job["href"]))
    return results

def scrape_google_jobs():
    r = requests.get(urls[1])
    soup = BeautifulSoup(r.text, "html.parser")
    results = []
    for link in soup.find_all("a"):
        title = link.text.strip()
        href = link.get("href", "")
        if is_relevant(title) and href.startswith("/jobs"):
            results.append(("Google", title, "https://careers.google.com" + href))
    return results

def save_csv(data):
    with open("results.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Company", "Title", "Link"])
        writer.writerows(data)

if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    data = []
    try:
        data.extend(scrape_linkedin(driver))
    except Exception as e:
        print(f"Error scraping LinkedIn: {e}")
    try:
        data.extend(scrape_google_jobs())
    except Exception as e:
        print(f"Error scraping Google: {e}")
    driver.quit()
    save_csv(data)
