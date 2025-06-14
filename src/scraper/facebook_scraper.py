# Facebook scraping logic stub
from facebook_scraper import get_posts

class Post:
    def __init__(self, post_id, text, images, comments):
        self.post_id = post_id
        self.text = text
        self.images = images or []
        self.comments = comments or []

class FacebookScraper:
    """
    Fetches recent posts from Facebook groups, skipping already seen ones.
    """
    def __init__(self, session):
        self.session = session
        self.seen_posts = set()

    def get_recent_posts(self, group_id, pages=1):
        posts = []
        for raw in get_posts(group=group_id, pages=pages):
            post_id = raw.get('post_id')
            if post_id in self.seen_posts:
                continue
            self.seen_posts.add(post_id)
            post = Post(
                post_id=post_id,
                text=raw.get('text', ''),
                images=raw.get('images', []),
                comments=raw.get('comments_full', [])
            )
            posts.append(post)
        return posts
