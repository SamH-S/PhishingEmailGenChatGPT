import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import re
import os
import sys
import logging
import string

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_directory(dir_name):
    """Create a directory if it does not exist."""
    os.makedirs(dir_name, exist_ok=True)
    return dir_name

def get_domain(url):
    """Extract domain name from URL."""
    return urlparse(url).netloc

def find_emails(text, regex_filter=None):
    """Use a regular expression to find all emails in the given text, optionally filtering by a custom regex."""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]{0,6}\.[A-Za-z]{2,6}(?=[\s\W])'
    emails = set(re.findall(email_pattern, text))
    if regex_filter:
        regex = re.compile(regex_filter)
        emails = {email for email in emails if regex.search(email)}
    return emails

def sanitize_filename(filename):
    """Sanitize and trim filename to valid characters and length."""
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    cleaned_filename = ''.join(c for c in filename if c in valid_chars)
    return cleaned_filename[:255]

def save_page_content(url, text, output_dir, emails):
    """Save the page text to a file named after the domain and each email in the specified directory."""
    domain = get_domain(url)
    for email in emails:
        filename = sanitize_filename(f"{domain}_{email}.txt")
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(text)
        logging.info(f"Saved page content where email was found to {filepath}")

def log_emails(emails, url, output_dir):
    """Log emails and the URL where they were found into a document in the specified directory."""
    filepath = os.path.join(output_dir, 'emails_found.txt')
    with open(filepath, 'a', encoding='utf-8') as file:
        for email in emails:
            file.write(f"{email}, {url}\n")

def scrape_page(url, origin_domain, depth, output_dir, visited, external_links_queue, regex_filter):
    """Scrape a single page and manage link collection."""
    if url in visited or depth > 2:  # Limit depth to prevent too deep recursion and irrelevant results
        return
    visited.add(url)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text()
        emails = find_emails(text_content, regex_filter)
        if emails:
            logging.info(f"Emails found on {url}: {emails}")
            save_page_content(url, text_content, output_dir, emails)
            log_emails(emails, url, output_dir)

        logging.info(f"Scraping URL: {url}, Depth: {depth}")
        for link in soup.find_all('a', href=True):
            link_url = urljoin(url, link['href'])
            if link_url not in visited and link_url.startswith('http'):
                current_domain = get_domain(link_url)
                if current_domain == origin_domain:
                    scrape_page(link_url, origin_domain, depth + 1, output_dir, visited, external_links_queue, regex_filter)
                else:
                    external_links_queue.append((link_url, 1))
    except Exception as e:
        logging.error(f"Error parsing HTML for URL {url}: {e}")

def get_all_urls(base_url, origin_domain, output_dir, regex_filter):
    """Manage the scraping of all URLs starting from the base URL."""
    visited = set()
    external_links_queue = []
    scrape_page(base_url, origin_domain, 0, output_dir, visited, external_links_queue, regex_filter)
    while external_links_queue:
        url, depth = external_links_queue.pop(0)
        scrape_page(url, origin_domain, depth, output_dir, visited, external_links_queue, regex_filter)

if __name__ == "__main__":
    if len(sys.argv) not in [2, 3]:
        logging.error("Usage: python script.py <URL> [regex_filter]")
        sys.exit(1)

    base_url = sys.argv[1]
    regex_filter = sys.argv[2] if len(sys.argv) == 3 else None
    origin_domain = get_domain(base_url)
    output_directory = create_directory('Scraper Output')
    get_all_urls(base_url, origin_domain, output_directory, regex_filter)
