import csv
import requests
from bs4 import BeautifulSoup
import concurrent.futures


def get_linkedin_url(company_name):
    company_name_no_spaces = company_name.replace(" ", "+")
    search_url = f"https://www.google.com/search?q={company_name_no_spaces}+linkedin"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find_all("a")

    for result in results:
        if (href := result.get("href")) and href.startswith("https://www.linkedin.com/"):
            return href
    return None


def write_company_urls_to_file(data_rows, output_file):
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company", "LinkedIn URL"])
        writer.writerows(data_rows)


def read_company_names(company_names_file):
    with open(company_names_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        return [row[0] for row in reader]


def create_rows_to_write(company_names, company_linkedin_urls):
    return list(zip(company_names, company_linkedin_urls)) or []


def main():
    company_names = read_company_names('./data/company_names.csv')

    with concurrent.futures.ThreadPoolExecutor() as executor:
        company_linkedin_urls = list(executor.map(get_linkedin_url, company_names))

    company_rows = create_rows_to_write(company_names, company_linkedin_urls)
    output_file = "./data/linkedin_urls.csv"
    write_company_urls_to_file(company_rows, output_file)


if __name__ == '__main__':
    main()
