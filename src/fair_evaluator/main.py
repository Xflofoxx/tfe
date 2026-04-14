import logging
from datetime import datetime
from pathlib import Path
from uuid import uuid4

import requests
import urllib3
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .db import Base, SessionLocal, engine
from .models import Fair, Settings
from .services.ollama import OllamaClient

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

app = FastAPI(title="Fiera Evaluator (Locale)", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

UPLOAD_DIR = Path("./data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR = Path("./data/reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
STRATEGY_DIR = Path("./data/strategy")
STRATEGY_DIR.mkdir(parents=True, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_settings_db(db: Session = Depends(get_db)):
    settings = db.query(Settings).first()
    if not settings:
        settings = Settings(ollama_url="http://localhost:11434", ollama_model="llama3.2")
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings


class FairCreate(BaseModel):
    fair_url: str
    site_url: str | None = ""
    linkedin_url: str | None = ""
    fair_email: str | None = ""
    folder_path: str | None = ""


class FairUpdate(BaseModel):
    name: str | None = None
    fair_url: str | None = None
    description: str | None = None
    folder_path: str | None = None
    dates: list[str] | None = None
    location: str | None = None
    target_segments: list[str] | None = None
    expected_visitors: int | None = None
    exhibitors_count: int | None = None
    fair_email: str | None = None
    stand_cost: int | None = None
    contacts: dict | None = None
    attachments: list | None = None
    status: str | None = None
    location: str | None = None
    dates: list[str] | None = None
    target_segments: list[str] | None = None
    recommendation: str | None = None
    rationale: str | None = None
    cost_estimate: dict | None = None
    ROI_assessment: dict | None = None
    historical_data: dict | None = None


class SettingsUpdate(BaseModel):
    ollama_url: str | None = None
    ollama_model: str | None = None
    strategy_prompt: str | None = None


# ============= SETTINGS =============

@app.get("/api/settings")
def get_settings_endpoint(db: Session = Depends(get_db)):
    s = get_settings_db(db)
    return {"ollama_url": s.ollama_url, "ollama_model": s.ollama_model, "strategy_prompt": s.strategy_prompt or ""}


@app.post("/api/settings")
def update_settings(settings: SettingsUpdate, db: Session = Depends(get_db)):
    s = get_settings_db(db)
    if settings.ollama_url is not None: s.ollama_url = settings.ollama_url
    if settings.ollama_model is not None: s.ollama_model = settings.ollama_model
    if settings.strategy_prompt is not None: s.strategy_prompt = settings.strategy_prompt
    db.commit()
    return {"status": "saved"}


@app.get("/api/settings/ollama-status")
def check_ollama_status(db: Session = Depends(get_db)):
    s = get_settings_db(db)
    try:
        resp = requests.get(f"{s.ollama_url}/api/tags", timeout=3)
        if resp.status_code == 200:
            models = resp.json().get("models", [])
            return {"status": "online", "available_models": [m.get("name", "") for m in models], "current_model": s.ollama_model}
    except Exception:
        pass
    return {"status": "offline", "available_models": []}


# ============= UPLOAD =============

@app.post("/api/upload-strategy")
async def upload_strategy(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.pdf'): raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    file_id = str(uuid4())
    file_path = STRATEGY_DIR / f"{file_id}_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    s = get_settings_db(db)
    s.strategy_pdf = str(file_path)
    db.commit()
    return {"file_path": str(file_path), "filename": file.filename}


class ExtractPdfRequest(BaseModel):
    pdf_path: str


@app.post("/api/extract-pdf")
def extract_pdf_data(data: ExtractPdfRequest, db: Session = Depends(get_db)):
    import os

    import fitz
    result = {"target_segments": [], "budget_range": None, "marketing_goals": []}
    pdf_path = data.pdf_path
    if not os.path.isabs(pdf_path): pdf_path = os.path.join(os.getcwd(), pdf_path)
    pdf_path = os.path.normpath(pdf_path)
try:
        doc = fitz.open(pdf_path)
        text = "\n".join([page.get_text() for page in doc])
        text_lower = text.lower()

        segments = []
        keywords = ["settore", "target", "segmento", "cliente", "azienda", "mercato", "pubblico"]
        for kw in keywords:
            if kw in text_lower:
                idx = text_lower.find(kw)
                snippet = text[idx:idx+200]
                if '\n' in snippet:
                    snippet = snippet[:snippet.find('\n')]
                if len(snippet) > 10:
                    segments.append(snippet.strip())
        result["target_segments"] = segments[:3]

        budget_keywords = ["budget", "eur", "euro", "costo", "spesa", "investimento"]
        for kw in budget_keywords:
            if kw in text_lower and "€" in text:
                import re
                matches = re.findall(r'\d+\.?\d*\s*(?:€|eur|euro)', text, re.IGNORECASE)
                if matches:
                    result["budget_range"] = f"€ {matches[0]}"
                    break

        goal_keywords = ["obiettivo", "goal", "brand", "lead", "visibilita", "network", "vendita"]
        for kw in goal_keywords:
            if kw in text_lower:
                idx = text_lower.find(kw)
                snippet = text[idx:idx+150]
                if '\n' in snippet:
                    snippet = snippet[:snippet.find('\n')]
                if len(snippet) > 10:
                    result["marketing_goals"].append(snippet.strip())
        result["marketing_goals"] = result["marketing_goals"][:3]
    except Exception as e:
        result["error"] = str(e)
    return result


@app.post("/api/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename or not file.filename.endswith('.pdf'): raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    file_id = str(uuid4())
    file_path = UPLOAD_DIR / f"{file_id}_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"file_path": str(file_path), "filename": file.filename, "file_id": file_id}


# ============= FAIR CRUD =============

@app.post("/api/fairs", response_model=dict)
def create_fair(fair_data: FairCreate, db: Session = Depends(get_db)):
    fair_id = str(uuid4())
    name = fair_data.fair_url
    if '://' in fair_data.fair_url: parts = fair_data.fair_url.split('/')
        name = parts[-1] if parts[-1] else parts[-2]
        if '.' in name: name = name.split('.')[0]

    fair = Fair(
        id=fair_id,
        name=name,
        url=fair_data.fair_url,
        company_website=fair_data.site_url or fair_data.fair_url,
        company_linkedin=fair_data.linkedin_url or None,
        fair_email=fair_data.fair_email or None,
        folder_path=fair_data.folder_path or None,
        status="in_valutazione",
        sources=[{"type": "manual", "url": fair_data.fair_url, "date": datetime.now().isoformat()}]
    )
    db.add(fair)
    db.commit()
    db.refresh(fair)
    return {"id": fair.id, "name": fair.name, "url": fair.url, "status": "created"}


@app.get("/api/fairs", response_model=list[dict])
def list_fairs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    fairs = db.query(Fair).order_by(Fair.id.desc()).offset(skip).limit(limit).all()
    return [{"id": f.id, "name": f.name or "N/A", "url": f.url or "", "description": f.description or "", "folder_path": f.folder_path or "", "site_url": f.company_website or "", "linkedin_url": f.company_linkedin or "", "fair_email": f.fair_email or "", "gallery": f.gallery or [], "attachments": f.attachments or [], "contacts": f.contacts or {}, "stand_cost": f.stand_cost or 0, "status": f.status or "in_valutazione", "scraped_data": f.scraped_data, "recommendation": f.recommendation or ""} for f in fairs]


@app.get("/api/fairs/{fair_id}", response_model=dict)
def get_fair(fair_id: str, db: Session = Depends(get_db)):
    fair = db.query(Fair).filter(Fair.id == fair_id).first()
    if not fair: raise HTTPException(status_code=404, detail="Fair not found")
    return {"id": fair.id, "name": fair.name, "url": fair.url, "description": fair.description or "", "folder_path": fair.folder_path or "", "site_url": fair.company_website, "dates": fair.dates, "location": fair.location, "target_segments": fair.target_segments, "expected_visitors": fair.expected_visitors, "exhibitors_count": fair.exhibitors_count, "sources": fair.sources, "linkedin_url": fair.company_linkedin, "fair_email": fair.fair_email or "", "gallery": fair.gallery or [], "attachments": fair.attachments or [], "contacts": fair.contacts or {}, "stand_cost": fair.stand_cost or 0, "status": fair.status or "in_valutazione", "scraped_data": fair.scraped_data, "historical_data": fair.historical_data, "ROI_assessment": fair.ROI_assessment, "cost_estimate": fair.cost_estimate, "recommendation": fair.recommendation, "rationale": fair.rationale, "report_pdf_path": fair.report_pdf_path, "report_html_path": fair.report_html_path, "venue": fair.venue, "address": fair.address, "sector": fair.sector, "frequency": fair.frequency, "edition": fair.edition, "organizer": fair.organizer, "exhibitor_countries": fair.exhibitor_countries, "visitor_profile": fair.visitor_profile, "product_categories": fair.product_categories, "key_features": fair.key_features}


@app.put("/api/fairs/{fair_id}", response_model=dict)
def update_fair(fair_id: str, fair_data: FairUpdate, db: Session = Depends(get_db)):
    fair = db.query(Fair).filter(Fair.id == fair_id).first()
    if not fair: raise HTTPException(status_code=404, detail="Fair not found")
    update_data = fair_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(fair, key, value)
    db.commit()
    db.refresh(fair)
    return {"id": fair.id, "status": "updated"}


@app.delete("/api/fairs/{fair_id}", response_model=dict)
def delete_fair(fair_id: str, db: Session = Depends(get_db)):
    fair = db.query(Fair).filter(Fair.id == fair_id).first()
    if not fair: raise HTTPException(status_code=404, detail="Fair not found")
    db.delete(fair)
    db.commit()
    return {"status": "deleted", "id": fair_id}


@app.post("/api/scrape-url")
def scrape_url(url_data: dict, db: Session = Depends(get_db)):
    """Quick scraping of a URL to get fair info before saving."""
    url = url_data.get("url", "")
    if not url: raise HTTPException(status_code=400, detail="URL required")

    settings = db.query(Settings).first()
    if not settings: settings = Settings()

    result = {"url": url, "text_content": "", "error": ""}

    try:
        import requests
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.9,it-IT;q=0.8,it;q=0.7'
        }
        resp = requests.get(url, timeout=15, verify=False, headers=headers, allow_redirects=True)
        html_content = resp.text

        if not html_content: result["error"] = "No content from requests"
        else:
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html_content, "html.parser")

                title = soup.find('title')
                result["title"] = title.text.strip() if title else ""

                meta_desc = soup.find('meta', attrs={'name': 'description'})
                result["description"] = meta_desc.get('content', '') if meta_desc else ""

                for script in soup(["script", "style", "nav", "footer", "header"]):
                    script.decompose()

                text_content = soup.get_text(separator=' ', strip=True)
                text_content = ' '.join(text_content.split())
                result["text_content"] = text_content[:3000]
                result["text_length"] = len(text_content)

            except Exception as e:
                result["error"] = f"Parse error: {str(e)}"

            ollama_available = False
            try:
                r = requests.get(f"{settings.ollama_url}/api/tags", timeout=3)
                ollama_available = r.status_code == 200
            except Exception:
        pass

            if ollama_available and settings.ollama_model: try:
                    from .services.ollama import OllamaClient
                    client = OllamaClient(settings.ollama_url)
                    model_name = str(settings.ollama_model)

                    prompt = f"""You are a trade fair analyzer. Extract information from this website text.

TEXT CONTENT:
{text_content[:6000]}

Extract in JSON format:
{{
  "name": "official fair name",
  "description": "2-3 sentence description",
  "location": "city",
  "dates": "dates if mentioned",
  "sector": "industry sector",
  "organizer": "organizer name",
  "venue": "venue name"
}}

Reply ONLY with valid JSON."""

                    result["prompt"] = prompt[:500] + "..."
                    ai_resp = client.chat(model_name, prompt)
                    result["ai_response"] = ai_resp[:300] + "..." if ai_resp and len(ai_resp) > 300 else ai_resp

                    if ai_resp: import json
                        import re
                        match = re.search(r'\{[\s\S]*\}', ai_resp)
                        if match: result["ai_data"] = json.loads(match.group())
                except Exception as e:
                    result["ai_error"] = str(e)
    except Exception as e:
        result["error"] = str(e)

    return result


# ============= ANALYZE =============

def analyze_fair_task(fair_id: str):
    """Background task per analisi fiera - web scraping + document analysis."""
    import json
    import re
    from datetime import datetime
    from pathlib import Path

    from bs4 import BeautifulSoup

    from .db import SessionLocal
    from .models import Fair, Settings
    from .services.ollama import OllamaClient

    db = SessionLocal()
    try:
        fair = db.query(Fair).filter(Fair.id == fair_id).first()
        if not fair: return

        settings = db.query(Settings).first()
        if not settings: settings = Settings()

        scraped_data = {}
        web_ai_data = {}

        # ============= 1. WEB SCRAPING =============
        url_to_check = fair.url or fair.company_website or ""
        if url_to_check: try:
                resp = requests.get(url_to_check, timeout=15, verify=False, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.9,it-IT;q=0.8,it;q=0.7'
                })
                if resp.status_code == 200: soup = BeautifulSoup(resp.text, "html.parser")

                    scraped_data['title'] = soup.find('title').text.strip() if soup.find('title') else ''
                    meta_desc = soup.find('meta', attrs={'name': 'description'})
                    scraped_data['description'] = meta_desc.get('content', '') if meta_desc else ''
                    og_title = soup.find('meta', attrs={'property': 'og:title'})
                    scraped_data['og_title'] = og_title.get('content', '') if og_title else ''
                    og_desc = soup.find('meta', attrs={'property': 'og:description'})
                    if og_desc: scraped_data['description'] = og_desc.get('content', '')
                    h1s = soup.find_all('h1')
                    scraped_data['h1'] = [h.text.strip() for h in h1s[:5]]
                    h2s = soup.find_all('h2')
                    scraped_data['h2'] = [h.text.strip() for h in h2s[:5]]
                    keywords = soup.find('meta', attrs={'name': 'keywords'})
                    scraped_data['keywords'] = keywords.get('content', '') if keywords else ''

                    all_links = []
                    for a in soup.find_all('a', href=True)[:20]:
                        all_links.append(a.get('href', ''))
                    scraped_data['links'] = all_links

                    main_text = ''
                    for p in soup.find_all(['p', 'div', 'span'])[:20]:
                        txt = p.get_text(strip=True)
                        if len(txt) > 20: main_text += txt + ' '
                    scraped_data['main_text'] = main_text[:2000]

                    scraped_data['source_url'] = url_to_check
                    scraped_data['scraped_at'] = datetime.now().isoformat()

                    ollama_available = False
                    try:
                        resp = requests.get(f"{settings.ollama_url}/api/tags", timeout=3)
                        ollama_available = resp.status_code == 200
                    except Exception:
        pass

                    if ollama_available and settings.ollama_model: try:
                            client = OllamaClient(settings.ollama_url)
                            model_name = str(settings.ollama_model) if settings.ollama_model else "phi: latest"

                            web_prompt = f"""You are a professional trade fair and exhibition analyzer. Analyze this fair's website content and extract ALL relevant information.

WEBSITE DATA:
- Title: {scraped_data.get('title', '')}
- Description: {scraped_data.get('description', '')}
- OG Title: {scraped_data.get('og_title', '')}
- H1 Tags: {scraped_data.get('h1', [])}
- H2 Tags: {scraped_data.get('h2', [])}
- Keywords: {scraped_data.get('keywords', '')}
- Main Text Sample: {scraped_data.get('main_text', '')[:1500]}

Extract in JSON format (be very thorough - extract every useful field):
{{
  "name": "official fair name (as used in official communications)",
  "description": "2-3 sentence description of the fair",
  "location": "city name",
  "venue": "venue/exhibition center name",
  "address": "full venue address",
  "dates": "exact dates (e.g., '15-18 March 2026' or 'October 2026')",
  "frequency": "annual/biennial/triennial/etc.",
  "edition": "edition number (e.g., '42nd')",
  "organizer": "organizing company name",
  "organizer_website": "organizer website",
  "organizer_email": "organizer email",
  "sector": "main industry sector",
  "target_segments": ["segment1", "segment2"],
  "expected_visitors": number (from text)",
  "exhibitors_count": number (from text)",
  "exhibitor_countries": ["country1", "country2"],
  "visitor_profile": "description of typical visitors",
  "product_categories": ["category1", "category2"],
  "key_features": ["feature1", "feature2"],
  "venue_address": "full venue address with postal code",
  "contact_email": "contact email",
  "contact_phone": "contact phone",
  "website": "official fair website URL"
}}

Reply ONLY with valid JSON. Use null for missing fields. Extract as much as possible from the content."""


                            ai_response = client.chat(model_name, web_prompt)
                            if ai_response: match = re.search(r'\{[\s\S]*\}', ai_response)
                                if match: web_ai_data = json.loads(match.group())
                                    scraped_data['web_ai_analyzed'] = {
                                        'data': web_ai_data,
                                        'analyzed_at': datetime.now().isoformat()
                                    }
                        except Exception as e:
                            scraped_data['web_ai_error'] = str(e)
            except Exception as e:
                scraped_data['error'] = str(e)

        doc_data = {}
        attachments = fair.attachments
        if attachments and isinstance(attachments, list): for att in attachments:
                if isinstance(att, dict): file_path = att.get('url', '')
                    file_name = att.get('name', '')

                    full_path = Path('.' + file_path) if file_path.startswith('/') else Path(file_path)

                    if not full_path.exists(): continue

                    ext = file_name.lower().split('.')[-1] if '.' in file_name else file_path.lower().split('.')[-1]
                    extracted_text = ''

                    if ext == 'pdf': try:
                            import pdfplumber
                            with pdfplumber.open(full_path) as pdf:
                                for page in pdf.pages[:5]:
                                    extracted_text += page.extract_text() or ''
                        except Exception as e:
                            scraped_data['pdf_error'] = str(e)
                            continue
                    elif ext == 'txt': try:
                            extracted_text = full_path.read_text(encoding='utf-8', errors='ignore')[:5000]
                        except Exception:
        pass
                    elif ext in ['doc', 'docx']: try:
                            from docx import Document
                            doc = Document(full_path)
                            for p in doc.paragraphs:
                                extracted_text += p.text + ' '
                        except Exception as e:
                            scraped_data['docx_error'] = str(e)
                            pass
                    elif ext in ['eml', 'msg']: try:
                            extracted_text = full_path.read_text(encoding='utf-8', errors='ignore')[:5000]
                        except Exception:
        pass
                    elif ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']: try:
                            import pytesseract
                            from PIL import Image
                            img = Image.open(full_path)
                            extracted_text = pytesseract.image_to_string(img)[:3000]
                        except Exception as e:
                            scraped_data['ocr_error'] = str(e)
                            pass

                    if extracted_text and len(extracted_text) > 30: ollama_available = False
                        try:
                            resp = requests.get(f"{settings.ollama_url}/api/tags", timeout=3)
                            ollama_available = resp.status_code == 200
                        except Exception:
        pass

                        if ollama_available and settings.ollama_model: try:
                                client = OllamaClient(settings.ollama_url)
                                model_name = str(settings.ollama_model) if settings.ollama_model else "phi: latest"

                                doc_prompt = f"""You are a professional trade fair and exhibition document analyzer. Extract ALL relevant information from this document (could be a PDF, email, brochure, or image text).

DOCUMENT CONTENT (first 4000 chars):
{extracted_text[:4000]}

Extract in JSON format (be very thorough):
{{
  "name": "official fair name",
  "description": "brief description",
  "location": "city name",
  "venue": "venue name",
  "address": "full venue address",
  "dates": "exact dates",
  "frequency": "annual/biennial/etc.",
  "edition": "edition number",
  "organizer": "organizer name",
  "organizer_email": "contact email",
  "sector": "industry sector",
  "target_segments": ["segment1", "segment2"],
  "expected_visitors": number,
  "exhibitors_count": number,
  "exhibitor_countries": ["country1", "country2"],
  "visitor_profile": "visitor description",
  "product_categories": ["category1", "category2"],
  "key_features": ["feature1", "feature2"],
  "stand_cost": "cost information if mentioned",
  "contact_name": "contact person name",
  "contact_email": "contact email",
  "contact_phone": "contact phone"
}}

Reply ONLY with valid JSON. Use null for missing fields."""


                                ai_response = client.chat(model_name, doc_prompt)
                                if ai_response: match = re.search(r'\{[\s\S]*\}', ai_response)
                                    if match: doc_data = json.loads(match.group())
                                        scraped_data['document_analyzed'] = {
                                            'file': file_name,
                                            'extracted_length': len(extracted_text),
                                            'data': doc_data,
                                            'analyzed_at': datetime.now().isoformat()
                                        }
                                        break
                            except Exception as e:
                                scraped_data['doc_ai_error'] = str(e)

        final_data = {**web_ai_data, **doc_data}

        if final_data.get('name'): fair.name = final_data['name']
        if final_data.get('description') and not fair.description: fair.description = final_data['description']
        if final_data.get('location'): fair.location = final_data['location']
        if final_data.get('venue'): fair.venue = final_data['venue']
        if final_data.get('address'): fair.address = final_data['address']
        if final_data.get('dates'): fair.dates = [final_data['dates']]
        if final_data.get('target_segments'): fair.target_segments = final_data['target_segments']
        if final_data.get('expected_visitors'): fair.expected_visitors = final_data['expected_visitors']
        if final_data.get('exhibitors_count'): fair.exhibitors_count = final_data['exhibitors_count']
        if final_data.get('frequency'): fair.frequency = final_data['frequency']
        if final_data.get('edition'): fair.edition = final_data['edition']
        if final_data.get('organizer'): fair.organizer = final_data['organizer']
        if final_data.get('sector'): fair.sector = final_data['sector']
        if final_data.get('exhibitor_countries'): fair.exhibitor_countries = final_data['exhibitor_countries']
        if final_data.get('visitor_profile'): fair.visitor_profile = final_data['visitor_profile']
        if final_data.get('product_categories'): fair.product_categories = final_data['product_categories']
        if final_data.get('key_features'): fair.key_features = final_data['key_features']

        scraped_data['final_data'] = final_data
        scraped_data['extracted_at'] = datetime.now().isoformat()

        fair.scraped_data = scraped_data
        if not fair.recommendation: fair.status = "in_valutazione"
        db.commit()

    except Exception:
        pass
    finally:
        db.close()


@app.post("/api/fairs/{fair_id}/analyze")
def analyze_fair(fair_id: str, db: Session = Depends(get_db)):
    """Avvia raccolta dati in background."""
    fair = db.query(Fair).filter(Fair.id == fair_id).first()
    if not fair: raise HTTPException(status_code=404, detail="Fair not found")

    import threading
    thread = threading.Thread(target=analyze_fair_task, args=(fair_id,))
    thread.daemon = True
    thread.start()

    return {"status": "started", "message": "Raccolta dati avviata in background"}


@app.post("/api/fairs/{fair_id}/evaluate")
def evaluate_fair(fair_id: str, db: Session = Depends(get_db)):
    """Valuta la fiera basandosi su strategia + allegati/preventivi caricati."""
    fair = db.query(Fair).filter(Fair.id == fair_id).first()
    if not fair: raise HTTPException(status_code=404, detail="Fair not found")

    attachments = fair.attachments
    has_attachments = False
    if attachments: if isinstance(attachments, list):
            has_attachments = len(attachments) > 0
        elif isinstance(attachments, str) and attachments.strip(): has_attachments = True

    if not has_attachments: raise HTTPException(status_code=400, detail="Caricare preventivi e allegati prima della valutazione")

    settings = get_settings_db(db)

    ollama_available = False
    try:
        import requests
        resp = requests.get(f"{settings.ollama_url}/api/tags", timeout=3)
        ollama_available = resp.status_code == 200
    except Exception:
        pass

    recommendation = None
    rationale = None
    roi = None

    if ollama_available and settings.ollama_model: try:
            from .services.ollama import OllamaClient
            model_name = str(settings.ollama_model) if settings.ollama_model else "phi: latest"
            client = OllamaClient(settings.ollama_url)

            context_parts = [f"Fair: {fair.name}", f"URL: {fair.url}"]
            if fair.description: context_parts.append(f"Description: {fair.description}")
            if fair.location: context_parts.append(f"Location: {fair.location}")
            if fair.dates: context_parts.append(f"Dates: {fair.dates}")
            if fair.expected_visitors: context_parts.append(f"Expected Visitors: {fair.expected_visitors}")
            if fair.exhibitors_count: context_parts.append(f"Exhibitors: {fair.exhibitors_count}")
            if fair.stand_cost: context_parts.append(f"Stand Cost: {fair.stand_cost} EUR")
            contacts_str = str(fair.contacts) if fair.contacts else "{}"
            context_parts.append(f"Contacts: {contacts_str}")

            attachments_count = len(attachments) if isinstance(attachments, list) else 0
            attachments_info = f"Attachments loaded: {attachments_count} files"
            context_parts.append(attachments_info)

            strategy_context = str(settings.strategy_prompt) if settings.strategy_prompt else ""

            prompt = f"""You are an expert in trade shows and events. Evaluate this trade fair based on the company strategy AND the attached quotes/documents.

COMPANY STRATEGY:
{strategy_context}

FAIR DATA:
{chr(10).join(context_parts)}

Based on your analysis:
1. Recommendation (RECOMMENDED / NOT RECOMMENDED / EVALUATE)
2. Brief rationale (2-3 sentences)
3. Estimated ROI assessment (low/medium/high)

Reply ONLY in JSON format:
{{"recommendation": "...", "rationale": "...", "roi_assessment": "..."}}"""

            ai_response = client.chat(model_name, prompt)
            if ai_response: import json
                import re
                match = re.search(r'\{[^}]+\}', ai_response, re.DOTALL)
                if match: result = json.loads(match.group())
                    recommendation = result.get('recommendation', '')
                    rationale = result.get('rationale', '')
                    roi = result.get('roi_assessment', '')
        except Exception:
        pass

    if recommendation: fair.recommendation = recommendation
    if rationale: fair.rationale = rationale
    if roi: fair.ROI_assessment = {"assessment": roi, "evaluated_at": datetime.now().isoformat()}

    db.commit()
    return {"status": "evaluated", "ollama_available": ollama_available, "recommendation": recommendation, "rationale": rationale}


# ============= REPORT =============

class ReportFormat(BaseModel):
    format: str = "html"


@app.post("/api/fairs/{fair_id}/report")
def generate_report(fair_id: str, fmt: ReportFormat = ReportFormat(format="html"), db: Session = Depends(get_db)):
    fair = db.query(Fair).filter(Fair.id == fair_id).first()
    if not fair: raise HTTPException(status_code=404, detail="Fair not found")
    settings = get_settings_db(db)
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader("./src/fair_evaluator/templates"))
    template = env.get_template("report.html")
    html_content = template.render(fair=fair, strategy_prompt=settings.strategy_prompt or "")
    html_path = REPORTS_DIR / f"report_{fair_id}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    fair.report_html_path = str(html_path)
    pdf_path = None
    if fmt.format.lower() == 'pdf': try:
            from weasyprint import HTML
            pdf_path = str(REPORTS_DIR / f"report_{fair_id}.pdf")
            HTML(string=html_content).write_pdf(pdf_path)
            fair.report_pdf_path = pdf_path
        except Exception:
        pass
    db.commit()
    return {"html": str(html_path), "pdf": pdf_path}


@app.get("/api/fairs/{fair_id}/report/download")
def download_report(fair_id: str, format: str = "html", db: Session = Depends(get_db)):
    fair = db.query(Fair).filter(Fair.id == fair_id).first()
    if not fair: raise HTTPException(status_code=404, detail="Fair not found")
    if format.lower() == "pdf" and fair.report_pdf_path: from pathlib import Path
        if Path(fair.report_pdf_path).exists(): return FileResponse(fair.report_pdf_path, filename=f"report_{fair_id}.pdf")
    if fair.report_html_path: from pathlib import Path
        if Path(fair.report_html_path).exists(): return FileResponse(fair.report_html_path, filename=f"report_{fair_id}.html")
    raise HTTPException(status_code=404, detail="Report not found")


# ============= IMPORT/EXPORT =============

@app.post("/api/import-excel-upload")
async def import_excel_upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    import io

    import openpyxl
    try:
        content = await file.read()
        wb = openpyxl.load_workbook(io.BytesIO(content))
        ws = wb.active
        headers = [str(h).lower().strip() if h else "" for h in next(ws.iter_rows(min_row=1, max_row=1, values_only=True))]
        col_idx = {h: i for i, h in enumerate(headers) if h}

        count = 0
        for row in ws.iter_rows(min_row=2, values_only=True):
            name = str(row[col_idx.get("nome", 0)]).strip() if col_idx.get("nome") is not None and len(row) > col_idx.get("nome", 0) and row[col_idx.get("nome", 0)] else ""
            url = str(row[col_idx.get("link evento", 0)]).strip() if col_idx.get("link evento") is not None and len(row) > col_idx.get("link evento", 0) and row[col_idx.get("link evento", 0)] else ""

            if not name and not url: continue

            if not name and url: if '/' in url:
                    name = url.split('/')[-1]
                    if '.' in name: name = name.split('.')[0]

            inizio = str(row[col_idx.get("inizio", 0)]).strip() if col_idx.get("inizio") is not None and len(row) > col_idx.get("inizio", 0) and row[col_idx.get("inizio", 0)] else ""
            fine = str(row[col_idx.get("fine", 0)]).strip() if col_idx.get("fine") is not None and len(row) > col_idx.get("fine", 0) and row[col_idx.get("fine", 0)] else ""
            dates = [inizio] if inizio else None

            contacts = {}
            contatto = str(row[col_idx.get("contatto", 0)]).strip() if col_idx.get("contatto") is not None and len(row) > col_idx.get("contatto", 0) and row[col_idx.get("contatto", 0)] else ""
            contatto_mail = str(row[col_idx.get("contatto mail", 0)]).strip() if col_idx.get("contatto mail") is not None and len(row) > col_idx.get("contatto mail", 0) and row[col_idx.get("contatto mail", 0)] else ""
            contatto_tel = str(row[col_idx.get("contatto tel", 0)]).strip() if col_idx.get("contatto tel") is not None and len(row) > col_idx.get("contatto tel", 0) and row[col_idx.get("contatto tel", 0)] else ""
            if contatto or contatto_mail or contatto_tel: contacts = {"name": contatto, "email": contatto_mail, "phone": contatto_tel}

            num_leads = row[col_idx.get("num. leads", 0)] if col_idx.get("num. leads") is not None and len(row) > col_idx.get("num. leads", 0) else None
            if isinstance(num_leads, str): try: num_leads = int(num_leads.replace('.', '').replace(',', ''))
                except: num_leads = None

            affluenza_2024 = row[col_idx.get("affluenza 2024", 0)] if col_idx.get("affluenza 2024") is not None and len(row) > col_idx.get("affluenza 2024", 0) else None
            affluenza_2025 = row[col_idx.get("affluenza 2025", 0)] if col_idx.get("affluenza 2025") is not None and len(row) > col_idx.get("affluenza 2025", 0) else None

            fair = Fair(
                id=str(uuid4()),
                name=name or "Fiera",
                url=url or None,
                location=str(row[col_idx.get("città", 0)]).strip() if col_idx.get("città") is not None and len(row) > col_idx.get("città", 0) and row[col_idx.get("città", 0)] else None,
                venue=str(row[col_idx.get("location", 0)]).strip() if col_idx.get("location") is not None and len(row) > col_idx.get("location", 0) and row[col_idx.get("location", 0)] else None,
                dates=dates,
                folder_path=str(row[col_idx.get("cartella", 0)]).strip() if col_idx.get("cartella") is not None and len(row) > col_idx.get("cartella", 0) and row[col_idx.get("cartella", 0)] else None,
                stand_cost=int(row[col_idx.get("costo stand", 0)]) if col_idx.get("costo stand") is not None and len(row) > col_idx.get("costo stand", 0) and row[col_idx.get("costo stand", 0)] and str(row[col_idx.get("costo stand", 0)]).isdigit() else 0,
                contacts=contacts if contacts else None,
                status=str(row[col_idx.get("stato", 0)]).strip() if col_idx.get("stato") is not None and len(row) > col_idx.get("stato", 0) and row[col_idx.get("stato", 0)] else "in_valutazione",
                scraped_data={"import_data": {"num_leads": num_leads, "affluenza_2024": affluenza_2024, "affluenza_2025": affluenza_2025}},
                sources=[{"type": "excel_import", "url": url, "date": datetime.now().isoformat()}]
            )
            db.add(fair)
            count += 1
        db.commit()
        wb.close()
        return {"status": "success", "count": count}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/export-excel")
def export_excel(db: Session = Depends(get_db)):

    import openpyxl
    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Fiere"
        ws.append(["Nome", "Città", "Location", "Stato", "Anno", "Inizio", "Fine", "Durata", "Countdown", "Cartella", "link evento", "Contatto", "Contatto mail", "Contatto tel", "Offerta", "Costo stand", "Data offerta", "Data approvazione", "Dimensioni stand", "Tipo stand", "Speech", "Target", "Num. Leads", "Affluenza 2024", "Affluenza 2025"])
        fairs = db.query(Fair).all()
        for fair in fairs:
            inizio = fair.dates[0] if fair.dates and len(fair.dates) > 0 else ""
            contatti = fair.contacts or {}
            num_leads = None
            aff_2024 = None
            aff_2025 = None
            if fair.scraped_data and isinstance(fair.scraped_data, dict): num_leads = fair.scraped_data.get('import_data', {}).get('num_leads')
                aff_2024 = fair.scraped_data.get('import_data', {}).get('affluenza_2024')
                aff_2025 = fair.scraped_data.get('import_data', {}).get('affluenza_2025')

            ws.append([
                fair.name or "",
                fair.location or "",
                fair.venue or "",
                fair.status or "in_valutazione",
                inizio[:4] if inizio else "",
                inizio,
                "",
                "",
                "",
                fair.folder_path or "",
                fair.url or "",
                contatti.get('name', ''),
                contatti.get('email', ''),
                contatti.get('phone', ''),
                "",
                fair.stand_cost or 0,
                "",
                "",
                "",
                "",
                "",
                "",
                num_leads,
                aff_2024,
                aff_2025
            ])
        output_file = REPORTS_DIR / f"Fiere_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        wb.save(output_file)
        return FileResponse(str(output_file), filename="Fiere.xlsx")
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ============= MAINTENANCE =============

@app.post("/api/db/clear")
def clear_database(db: Session = Depends(get_db)):
    try:
        db.query(Fair).delete()
        db.commit()
        return {"status": "success", "message": "Database cleared"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/db/stats")
def get_database_stats(db: Session = Depends(get_db)):
    total = db.query(Fair).count()
    in_valutazione = db.query(Fair).filter(Fair.status == "in_valutazione").count()
    approvata = db.query(Fair).filter(Fair.status == "approvata").count()
    in_gestione = db.query(Fair).filter(Fair.status == "in_gestione").count()
    conclusa = db.query(Fair).filter(Fair.status == "conclusa").count()
    rifiutata = db.query(Fair).filter(Fair.status == "rifiutata").count()

    fairs = db.query(Fair).all()
    total_contacts = {"cold": 0, "warm": 0, "hot": 0}
    contacts_by_fair = []
    total_stand_cost = 0

    for fair in fairs:
        if fair.contacts: cold = fair.contacts.get("cold", 0)
            warm = fair.contacts.get("warm", 0)
            hot = fair.contacts.get("hot", 0)
            total_contacts["cold"] += cold
            total_contacts["warm"] += warm
            total_contacts["hot"] += hot
            contacts_by_fair.append({"name": fair.name, "cold": cold, "warm": warm, "hot": hot})
        if fair.stand_cost: total_stand_cost += fair.stand_cost

    return {
        "total": total,
        "in_valutazione": in_valutazione,
        "approvata": approvata,
        "in_gestione": in_gestione,
        "conclusa": conclusa,
        "rifiutata": rifiutata,
        "contacts": total_contacts,
        "contacts_by_fair": contacts_by_fair,
        "total_stand_cost": total_stand_cost
    }


@app.post("/api/strategy/load")
async def load_strategy_prompt(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    prompt_content = content.decode("utf-8")

    settings = get_settings_db(db)
    settings.strategy_prompt = prompt_content
    db.commit()

    prompt_file = STRATEGY_DIR / "generated_prompt.txt"
    with open(prompt_file, "w", encoding="utf-8") as f:
        f.write(prompt_content)

    return {"status": "success", "prompt": prompt_content}


@app.post("/api/strategy/analyze")
def analyze_strategy_manual(db: Session = Depends(get_db)):
    import glob
    pdf_files = glob.glob(str(STRATEGY_DIR / "*.pdf"))
    if not pdf_files: return {"status": "error", "message": "Nessun file PDF trovato"}

    settings = get_settings_db(db)
    client = OllamaClient(str(settings.ollama_url) if settings.ollama_url else "http://localhost: 11434")

    prompt = f"""Il file PDF della strategia marketing si trova in: {pdf_files[0]}

Poiche il PDF non e leggibile automaticamente, crea un prompt di strategia generico basato su:
- Settore: Tecnologia B2B, software per retail/GDO
- Target: CTO, Manager IT, Responsabili acquisti retail
- Budget: 15000 euro/fiera
- Obiettivi: lead, brand awareness, networking
- Geografie: Italia, Europa

Genera un prompt dettagliato in italiano per valutare le fiere."""

    try:
        response = client.chat(str(settings.ollama_model) if settings.ollama_model else "phi: latest", prompt)
        if response: settings.strategy_prompt = response
            db.commit()
            prompt_file = STRATEGY_DIR / "generated_prompt.txt"
            with open(prompt_file, "w", encoding="utf-8") as f:
                f.write(response)
            return {"status": "success", "prompt": response}
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {"status": "error", "message": "Impossibile generare il prompt"}
def analyze_strategy_pdf(db: Session = Depends(get_db)):
    import glob
    pdf_files = glob.glob(str(STRATEGY_DIR / "*.pdf"))
    if not pdf_files: return {"status": "error", "message": "Nessun file PDF trovato in data/strategy"}

    settings = get_settings_db(db)
    ollama_url = str(settings.ollama_url) if settings.ollama_url else "http://localhost: 11434"
    model_name = str(settings.ollama_model) if settings.ollama_model else "phi: latest"

    client = OllamaClient(ollama_url)

    generated_prompts = []

    for pdf_file in pdf_files:
        prompt = f"""Leggi il documento PDF disponibile in: {pdf_file}

Estrai le informazioni chiave sulla strategia marketing:
1. Settore/Industria di riferimento
2. Target cliente (B2B/B2C, dimensione aziende)
3. Obiettivi di marketing (lead, brand awareness, vendite)
4. Budget indicativo
5. Eventuali fiere o eventi di interesse
6. Geografie target

Genera un prompt dettagliato che un agente AI potra usare per valutare le fiere in base a questa strategia. Il prompt deve essere in italiano e contenere almeno 5 punti specifici."""

        try:
            response = client.chat(model_name, prompt)
            if response: generated_prompts.append({
                    "file": pdf_file,
                    "prompt": response
                })
        except Exception as e:
            generated_prompts.append({
                "file": pdf_file,
                "error": str(e)
            })

    if generated_prompts and "prompt" in generated_prompts[0]: best_prompt = generated_prompts[0]["prompt"]
        settings.strategy_prompt = best_prompt
        db.commit()

        prompt_file = STRATEGY_DIR / "generated_prompt.txt"
        with open(prompt_file, "w", encoding="utf-8") as f:
            f.write(best_prompt)

        return {"status": "success", "prompt": best_prompt, "saved_to": str(prompt_file)}

    return {"status": "error", "message": "Impossibile generare il prompt. Verificare che Ollama sia attivo.", "details": generated_prompts}


# ============= UI PAGES =============

TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"


def render_template(template_name: str, **kwargs) -> str:
    template_path = TEMPLATE_DIR / template_name
    if template_path.exists(): with open(template_path, encoding="utf-8") as f:
            return f.read()
    return f"<h1>Template {template_name} not found</h1>"


@app.get("/", response_class=HTMLResponse)
def home_page():
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("page_home.html")
    stats = get_database_stats(SessionLocal())
    ollama = check_ollama_status(SessionLocal())
    settings = get_settings_endpoint(SessionLocal())
    return HTMLResponse(template.render(stats=stats, ollama=ollama, settings=settings, nav_active="home"))


@app.get("/fairs", response_class=HTMLResponse)
def fairs_list_page():
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("page_fairs.html")
    db = SessionLocal()
    fairs = db.query(Fair).order_by(Fair.id.desc()).limit(100).all()
    locations = sorted(set(f.location for f in fairs if f.location))
    years = set()
    for f in fairs:
        if f.dates and f.dates[0]: years.add(f.dates[0][:4])
    years = sorted([y for y in years if y], reverse=True)
    return HTMLResponse(template.render(fairs=fairs, locations=locations, years=years, nav_active="fairs"))


@app.get("/fairs/new", response_class=HTMLResponse)
def new_fair_page():
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("page_fair_new.html")
    return HTMLResponse(template.render(nav_active="fairs"))


@app.get("/fairs/{fair_id}", response_class=HTMLResponse)
def fair_detail_page(fair_id: str):
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("page_fair_detail.html")
    fair = get_fair(fair_id, SessionLocal())
    return HTMLResponse(template.render(fair=fair, nav_active="fairs"))


@app.get("/settings", response_class=HTMLResponse)
def settings_page():
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("page_settings.html")
    settings = get_settings_endpoint(SessionLocal())
    ollama = check_ollama_status(SessionLocal())
    return HTMLResponse(template.render(settings=settings, ollama=ollama, nav_active="settings"))


@app.get("/maintenance", response_class=HTMLResponse)
def maintenance_page():
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("page_maintenance.html")
    stats = get_database_stats(SessionLocal())
    settings = get_settings_endpoint(SessionLocal())
    return HTMLResponse(template.render(stats=stats, strategy_prompt=settings.get('strategy_prompt', ''), nav_active="maintenance"))


# Legacy
@app.post("/fair-scan")
def fair_scan(fair_data: FairCreate, db: Session = Depends(get_db)):
    return create_fair(fair_data, db)


# Static files
DATA_DIR = Path("./data")
app.mount("/data", StaticFiles(directory=str(DATA_DIR.absolute())))


@app.get("/api/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}
