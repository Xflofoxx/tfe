import argparse
from importlib import import_module

from fastapi.testclient import TestClient


def main():
    parser = argparse.ArgumentParser(description="Valutatore di fiere - CLI (locale)")
    subparsers = parser.add_subparsers(dest="cmd")

    scan_p = subparsers.add_parser("scan", help="Ingestione rapida di una fiera")
    scan_p.add_argument("fair_url", help="URL della fiera")
    scan_p.add_argument("marketing_pdf", nargs="?", default="", help="Percorso locale al PDF di marketing strategy")
    scan_p.add_argument("site_url", nargs="?", default="", help="URL sito fiera")
    scan_p.add_argument("linkedin_url", nargs="?", default="", help="LinkedIn organizzatore")

    report_p = subparsers.add_parser("report", help="Genera report per una fiera esistente")
    report_p.add_argument("fair_id", help="ID della fiera")
    report_p.add_argument("format", choices=["pdf", "html", "both"], default="html", help="Formato report")

    args = parser.parse_args()
    # Import app module dynamically from src.fair_evaluator.main
    module = import_module("src.fair_evaluator.main")
    client = TestClient(module.app)

    if args.cmd == "scan":
        payload = {
            "fair_url": args.fair_url,
            "marketing_pdf": args.marketing_pdf,
            "site_url": args.site_url,
            "linkedin_url": args.linkedin_url,
        }
        resp = client.post("/fair-scan", json=payload)
        print(resp.json())
    elif args.cmd == "report":
        resp = client.post(f"/fairs/{args.fair_id}/report", json={"format": args.format})
        print(resp.json())
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
