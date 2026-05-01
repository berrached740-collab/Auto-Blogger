import os
import random
import feedparser
import re
import google.generativeai as genai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# --- 1. إعدادات الروابط (RSS) ---
rss_urls = [
    "https://cointelegraph.com/rss",
    "https://search.cnbc.com/rs/search/combinedcms/view.xml?profile=MARKET_UPDATE",
    "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
    "https://www.coindesk.com/arc/outboundfeeds/rss/?category=markets",
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://www.wired.com/feed/rss",
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "http://rss.cnn.com/rss/edition.rss",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "http://rssfeeds.webmd.com/rss/rss.aspx?RSSSource=RSS_PUBLIC",
    "https://www.healthline.com/rss"
]

# --- 2. إعدادات المتغيرات (الروابط والمفاتيح) ---
BLOG_ID = os.environ.get("BLOG_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
# ضع الرابط المباشر الخاص بإعلاناتك (Adsterra) هنا بين علامتي التنصيص
ADSTERRA_LINK = "https://www.google.com"

# --- 3. دالة جلب الأخبار ---
def get_random_news():
    random.shuffle(rss_urls)
    for url in rss_urls:
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                entry = random.choice(feed.entries[:5])
                return entry.title, entry.description, entry.link
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            continue
    return None, None, None

# --- 4. دالة صياغة المقال بالذكاء الاصطناعي (باللغة الإنجليزية) ---
def rewrite_article(title, description):
    genai.configure(api_key=GEMINI_API_KEY)
    # استخدام الموديل الأسرع والأفضل للمقالات
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    You are a professional SEO blog writer. Write an engaging, unique, and highly readable article in English based on the following news:
    Title: {title}
    Details: {description}
    
    Requirements:
    1. Write a catchy headline wrapped in <h1> tag.
    2. Write well-structured paragraphs using HTML tags (<h2>, <p>, <strong>).
    3. Include a short conclusion.
    Do not use markdown code blocks like ```html. Output raw HTML only.
    """
    response = model.generate_content(prompt)
    return response.text

# --- 5. دالة النشر على بلوجر ---
def post_to_blogger(title, content, source_link):
    # قراءة مفتاح الدخول الدائم الذي استخرجناه سابقاً
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('blogger', 'v3', credentials=creds)
    
    # تصميم زر الإعلان (Smart Link)
    ad_button = f'''
    <br><br>
    <div style="text-align: center;">
        <a href="    adsterra_direct_link = "https://www.profitablecpmratenetwork.com/ve3ktt21?key=949627e2df43786ddffa0da016c1bdcb"
" target="_blank" style="background-color: #ff0000; color: white; padding: 15px 25px; text-decoration: none; font-size: 18px; border-radius: 5px; font-weight: bold;">Click Here for More Info</a>
    </div>
    <br>
    <p><em><a href="{source_link}" rel="nofollow" target="_blank">Source</a></em></p>
    '''
    
    final_content = content + ad_button
    
    body = {
        "kind": "blogger#post",
        "title": title,
        "content": final_content
    }
    
    posts = service.posts()
    result = posts.insert(blogId=BLOG_ID, body=body, isDraft=False).execute()
    print(f"Post published successfully! Link: {result.get('url')}")

# --- 6. التشغيل الرئيسي ---
if __name__ == "__main__":
    print("Fetching news...")
    original_title, desc, link = get_random_news()
    
    if original_title:
        print(f"Original Title: {original_title}")
        print("Rewriting with Gemini AI...")
        
        new_content = rewrite_article(original_title, desc)
        
        # محاولة استخراج العنوان الجديد من المقال، وإلا نستخدم القديم
        match = re.search(r'<h1>(.*?)</h1>', new_content, re.IGNORECASE)
        if not match:
            match = re.search(r'<h2>(.*?)</h2>', new_content, re.IGNORECASE)
            
        post_title = match.group(1) if match else original_title
        
        print("Publishing to Blogger...")
        post_to_blogger(post_title, new_content, link)
    else:
        print("No news found.")
