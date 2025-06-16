from dotenv import load_dotenv
load_dotenv()
print("🚀 Deal Finder starting up...")
from auth.session_manager import FacebookSession
from scraper.facebook_scraper import FacebookScraper
from parser.post_analyzer import PostAnalyzer
from valuation.valuation_client import ValuationClient
from notification.notifier import Notifier
import schedule
import time
import yaml
import datetime

# Load config
def load_cfg():
    with open('config/config.yaml') as f:
        return yaml.safe_load(f)

cfg = load_cfg()

session = FacebookSession(cfg['facebook']['cookie_file'])
scraper = FacebookScraper(session)
analyzer = PostAnalyzer(cfg['keywords'])
valuator = ValuationClient()
notifier = Notifier()  # now reads Twilio creds from .env

def job():
    print(f"🚀 Starting scraping job at {datetime.datetime.now()}")
    for group_id in cfg['facebook']['groups']:
        print(f"🔍 Scraping group: {group_id}")
        # Pull 3 pages instead of the default 1–2 to get more posts
        posts = scraper.get_recent_posts(group_id, pages=3)
        print(f"   Found {len(posts)} posts in this run")
        for post in posts:
            if not analyzer.is_relevant(post.text):
                continue
            print(f"   Processing post ID: {post.post_id}")
            card = analyzer.extract_details(post)
            assessment = valuator.assess_deal(card)
            print(f"   Valuation → deal: {assessment.is_good_deal}, est_value: {assessment.estimated_value}")
            if assessment.is_good_deal:
                msg = f"Deal found: {card['year']} {card['player']} {card['set']} for ${card['price']}"
                notifier.send_whatsapp(msg)
                print(f"   🔔 Sent alert: {msg}")
    print(f"✅ Completed scraping job at {datetime.datetime.now()}\n") 

# Schedule
schedule.every(cfg['scheduler']['interval_minutes']).minutes.do(job)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)

