from auth.session_manager import FacebookSession
from scraper.facebook_scraper import FacebookScraper
from parser.post_analyzer import PostAnalyzer
from valuation.valuation_client import ValuationClient
from notification.notifier import Notifier
import schedule
import time
import yaml

# Load config
with open('config/config.yaml') as f:
    cfg = yaml.safe_load(f)

session = FacebookSession(cfg['facebook']['cookie_file'])
scraper = FacebookScraper(session)
analyzer = PostAnalyzer(cfg['keywords'])
valuator = ValuationClient()
notifier = Notifier(cfg['twilio'])

def job():
    for group_id in cfg['facebook']['groups']:
        posts = scraper.get_recent_posts(group_id)
        for post in posts:
            if not analyzer.is_relevant(post.text):
                continue
            card_data = analyzer.extract_details(post)
            assessment = valuator.assess_deal(card_data)
            if assessment.is_good_deal:
                msg = f"Deal: {card_data['player']} {card_data['set']} for ${card_data['price']}"
                notifier.send_whatsapp(msg)

# Schedule
schedule.every(cfg['scheduler']['interval_minutes']).minutes.do(job)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
