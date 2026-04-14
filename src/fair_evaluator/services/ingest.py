import requests
from bs4 import BeautifulSoup as _BS

PDF_EXTS = {".pdf", ".PDF"}


def extract_text_from_url(url: str) -> str:
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code != 200:
            return ""
        return resp.text
    except Exception:
        return ""


def extract_text_from_html(html: str) -> str:
    soup = _BS(html, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    return soup.get_text(separator=" ")


def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        import fitz  # PyMuPDF
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
    html = extract_text_from_url(url)
    if not html:
        return ""
    return extract_text_from_html(html)

def ingest_fair_metadata(fair_url: str, marketing_pdf_path: str, site_url: str, linkedin_url: str):
    data = {
        'name': None,
        'url': fair_url,
        'dates': None,
        'location': None,
        'target_segments': None,
        'exhibitors_count': None,
        'expected_visitors': None,
        'sources': [],
        'marketing_strategy_pdf': marketing_pdf_path,
        'site_url': site_url,
        'linkedin_url': linkedin_url,
        'marketing_text': None,
        'historical_data': None,
        'ROI_assessment': None,
        'cost_estimate': None,
        'recommendation': None,
        'rationale': None,
    }
    if marketing_pdf_path:
        data['marketing_text'] = extract_text_from_pdf(marketing_pdf_path)
    return data
