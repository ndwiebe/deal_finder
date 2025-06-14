# Post filtering and parsing logic stub
import re
import requests
from io import BytesIO
from PIL import Image
import pytesseract

class PostAnalyzer:
    """
    Filters posts by keywords and extracts structured card details (price, year, player, set, grade).
    """
    def __init__(self, keywords):
        self.keywords = [kw.lower() for kw in keywords]
        self.price_regex = re.compile(r'\$?\d+(?:[.,]\d+)?')
        self.year_regex = re.compile(r'\b(?:19|20)\d{2}\b')
        self.grade_regex = re.compile(r'\b(PSA|BGS|SGC)\s*\d+\b', re.IGNORECASE)

    def is_relevant(self, text: str) -> bool:
        t = text.lower()
        has_kw = any(kw in t for kw in self.keywords)
        has_price = bool(self.price_regex.search(t))
        return has_kw and has_price

    def extract_details(self, post):
        text = post.text
        # Price
        price_match = self.price_regex.search(text)
        price = float(price_match.group(0).replace('$','').replace(',','')) if price_match else None
        # Fallback to OCR if needed
        if price is None and post.images:
            price = self._ocr_price(post.images[0])
        # Year
        year_match = self.year_regex.search(text)
        year = int(year_match.group(0)) if year_match else None
        # Grade
        grade_match = self.grade_regex.search(text)
        grade = grade_match.group(0).upper() if grade_match else None
        # Description before price
        desc = text
        if price_match:
            desc = text[:price_match.start()]
        desc = re.sub(r'\bFS\b:?', '', desc, flags=re.IGNORECASE)
        desc = re.sub(r'\bFT\b:?', '', desc, flags=re.IGNORECASE)
        desc = desc.strip(' -:\n')
        # Heuristic player/set extraction
        words = desc.split()
        player = None
        set_name = None
        if year and str(year) in words:
            idx = words.index(str(year))
            if idx+1 < len(words):
                player = words[idx+1]
            if idx+2 < len(words):
                set_name = words[idx+2]
        if not player and len(words) >= 2:
            player = ' '.join(words[:2])
        elif not player and words:
            player = words[0]
        if not set_name and len(words) >= 3:
            set_name = words[2]
        return {
            'year': year,
            'player': player,
            'set': set_name,
            'grade': grade,
            'price': price,
            'description': desc
        }

    def _ocr_price(self, image_url: str):
        try:
            resp = requests.get(image_url)
            img = Image.open(BytesIO(resp.content))
            text = pytesseract.image_to_string(img)
            match = self.price_regex.search(text)
            if match:
                return float(match.group(0).replace('$','').replace(',',''))
        except Exception as e:
            print(f"OCR error: {e}")
        return None
