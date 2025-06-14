# Sports Card Deal Finder

Automated tool to monitor Facebook groups for sports card sales, evaluate deals via a GPT-based model, and notify you over WhatsApp.

## Features
- Runs every X minutes (configurable)
- Session-based Facebook authentication
- Keyword & regex filtering
- OCR price extraction
- GPT valuation via custom prompt
- WhatsApp alerts via Twilio

## Setup
1. Copy `config/config.yaml.example` to `config/config.yaml` and fill in credentials.
2. `pip install -r requirements.txt`
3. Optionally build and run via Docker: `docker build -t deal-finder . && docker run deal-finder`
4. Start the service: `./scripts/run.sh`

## Folder Layout
See the GitHub repository structure in this zip.
