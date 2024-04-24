# Python Email Scraper and Generator

This repository contains two Python scripts: `scraper.py` for scraping websites to find email addresses, and `emailgen.py` for generating customised phishing emails based on scraped page content through ChatGPT.
This is a proof of concept to encourage discussion. I'd expect the following improvements to be made by criminals:
- Instead of providing a payload link or file within the first email, leveraging ChatGPT to have an email back and fourth to develop a raport before introducing the payload. By the fourth email, most people would no longer have their guard up.
- Searching for further information associated with the recipients to tailor the phishing email content to them. For instance, a phishing email may mention a convention the target may have been present at.
- Testing out different prompts to hone in on which instructions are best to feed to AI tools to make the most effective phishing attempt.

## scraper.py

### Description
This script is designed to scrape web pages to find email addresses and save both the page content and the emails found. It includes functionality to handle recursion up to a defined depth and manage external links.

### Usage
`python scraper.py <URL> [regex_filter]`

- `<URL>`: The base URL from which scraping should start.
- `[regex_filter]`: Optional. A regex pattern to filter the email addresses.

### Features
- Depth-limited recursive scraping
- Email extraction with optional filtering
- Saves emails and their corresponding page content locally
- Logs actions to facilitate debugging

### Dependencies
- `requests`
- `bs4` (BeautifulSoup)
- `re`, `os`, `sys`, `logging`, `urllib.parse`, `time`, `string`

---

## emailgen.py

### Description
This script reads the text files containing page content, extracts email addresses, and uses an ChatGPT to generate convincing email content aimed at prompting recipients to click on a link.

### Usage
`python emailgen.py <API_key> <target_directory>`

- `<API_key>`: Your API key for accessing ChatGPT.
- `<target_directory>`: The directory containing text files with page content.

### Features
- Extracts emails from text files
- Generates custom email content using AI
- Saves the generated emails in a timestamped directory

### Dependencies
- `os`, `sys`, `logging`, `re`, `datetime`, `subprocess`, `json`

---

## Setup

1. Clone this repository.
2. Install required packages:
pip install requests beautifulsoup4


## Notes

For more details, refer to the scripts' source code and comments.
