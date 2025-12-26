# Pulse Review Scraper

This project scrapes SaaS product reviews and saves them as JSON.

## Features
- Choose review source:
  - Trustpilot (fully working)
  - G2 (it may return 403 due to bot protection)
  - Capterra (it may return 403 due to bot protection)
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
G2 and Capterra employ strong bot-protection systems which block non-browser traffic (403). Instead of attempting to bypass security — which may violate TOS — the script detects blocking and exits gracefully. A 3rd SaaS review source was implemented to ensure functionality within ethical and technical constraints.

->Some platforms block bots.  
->The script does NOT bypass security.  
->Trustpilot works fully to demonstrate functionality.
