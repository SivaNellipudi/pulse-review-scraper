# Pulse Review Scraper

This project scrapes SaaS product reviews and saves them as JSON.

## Features
- Choose review source:
  - Trustpilot ✅ (fully working)
  - G2 🚧 (may return 403 due to bot protection)
  - Capterra 🚧 (may return 403 due to bot protection)
- Input date range
- Pagination support
- JSON output
- Graceful error handling

## Tech Used
Python, Requests, BeautifulSoup, lxml

## How To Run

1. Install dependencies  
   pip install -r requirements.txt

2. Run the script  
   python main.py

3. Select source and enter details  
   Output JSON will be saved in the project folder.

## Notes
Some platforms block bots.  
The script does NOT bypass security.  
Trustpilot works fully to demonstrate functionality.