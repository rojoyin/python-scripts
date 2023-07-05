import csv
import time

from playwright.sync_api import sync_playwright


def read_g2_company_urls(g2crowdurls_file):
    with open(g2crowdurls_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        return [row[0] for row in reader]


def scrape_company_details(company_url):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        context.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })
        page.goto(f"{company_url}#reviews")
        time.sleep(10)
        company_name = page.inner_text(".c-midnight-100")
        rating = page.inner_text(".fw-semibold")
        reviews = page.inner_text(".l2 .mb-half")
        description = page.inner_text(".ws-pw")
        results.append({
            "Company Name": company_name,
            "Rating": rating,
            "Reviews": reviews,
            "Description": description
        })
        page.close()
        browser.close()

    return results


for url in read_g2_company_urls('./data/g2crowdurls.csv'):
    print(scrape_company_details(url))
