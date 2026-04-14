import subprocess
import tempfile
from pathlib import Path

import requests
from bs4 import BeautifulSoup as _BS

PDF_EXTS = {".pdf", ".PDF"}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,it-IT;q=0.8,it;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


def _fetch_with_curl(url: str) -> str:
    """Fetch URL using curl for better JS handling."""
    try:
        result = subprocess.run(
            ["curl", "-s", "-L", "--max-time", "30", "-A", HEADERS["User-Agent"], url],
            capture_output=True,
            text=True,
            timeout=35,
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout
    except Exception:
        pass
    return ""


def _fetch_with_playwright(url: str) -> str:
    """Fetch URL using Playwright (headless browser) for JavaScript-heavy sites."""
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(user_agent=HEADERS["User-Agent"])
            page.goto(url, timeout=30000, wait_until="networkidle")
            content = page.content()
            browser.close()
            return content
    except Exception:
        pass
    return ""


def extract_text_from_url(url: str) -> str:
    """Fetch URL content using multiple methods."""
    html = ""

    html = _fetch_with_curl(url)
    if html:
        return html

    try:
        resp = requests.get(url, timeout=15, headers=HEADERS, verify=False)
        if resp.status_code == 200:
            return resp.text
    except Exception:
        pass

    return ""


def extract_text_from_html(html: str) -> str:
    """Clean HTML and extract text content."""
    soup = _BS(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()
    for tag in soup.find_all("noscript"):
        tag.decompose()
    text = soup.get_text(separator=" ")
    return " ".join(text.split())


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF file."""
    try:
        import fitz
    except Exception:
        return ""
    try:
        doc = fitz.open(pdf_path)
        text = []
        for page in doc:
            text.append(page.get_text())
        doc.close()
        return "\n".join(text)
    except Exception:
        return ""


def scrape_text_from_site(url: str) -> str:
    """Scrape text from website using curl/requests fallback."""
    html = extract_text_from_url(url)
    if not html:
        return ""
    return extract_text_from_html(html)


def scrape_with_browser(url: str) -> str:
    """Scrape using headless browser for JS-heavy sites."""
    html = _fetch_with_playwright(url)
    if html:
        return extract_text_from_html(html)
    return scrape_text_from_site(url)


def ingest_fair_metadata(fair_url: str, marketing_pdf_path: str, site_url: str, linkedin_url: str):
    """Ingest fair metadata from various sources."""
    data = {
        "name": None,
        "url": fair_url,
        "dates": None,
        "location": None,
        "target_segments": None,
        "exhibitors_count": None,
        "expected_visitors": None,
        "sources": [],
        "marketing_strategy_pdf": marketing_pdf_path,
        "site_url": site_url,
        "linkedin_url": linkedin_url,
        "marketing_text": None,
        "historical_data": None,
        "ROI_assessment": None,
        "cost_estimate": None,
        "recommendation": None,
        "rationale": None,
    }
    if marketing_pdf_path:
        data["marketing_text"] = extract_text_from_pdf(marketing_pdf_path)
    return data
