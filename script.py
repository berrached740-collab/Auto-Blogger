import os
import feedparser
import google.generativeai as genai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import random

def main():
    print("🚀 Starting the Script...")

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found")
        return
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

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
    
    news_title = ""
    news_image_url = ""
    
    # اختيار مصدر عشوائي لتنويع الأخبار
    random.shuffle(rss_urls)
    
    # محاولة العثور على خبر جديد وصورته
    for url in rss_urls:
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                # اختيار خبر عشوائي من أول 5 أخبار لتفادي التكرار
                latest_entry = random.choice(feed.entries[:5])
                news_title = latest_entry.title
                
                # محاولة سحب الصورة المرفقة مع الخبر
                if 'media_content' in latest_entry and len(latest_entry.media_content) > 0:
                    news_image_url = latest_entry.media_content[0]['url']
                elif 'links' in latest_entry:
                    for link in latest_entry.links:
                        if 'image' in link.get('type', ''):
                            news_image_url = link.href
                            break
                break
        except:
            continue
            
    if not news_title:
        print("❌ No news found today.")
        return
        
    print(f"📰 Found new article: {news_title}")
    if news_image_url:
        print(f"📸 Found image for the article: {news_image_url}")

    # ====================================================
    # 🔴 هام: رابط Adsterra المباشر الخاص بك 
    # ====================================================
    adsterra_direct_link = "https://www.profitablecpmratenetwork.com/ve3ktt21?key=949627e2df43786ddffa0da016c1bdcb"

    # أمر الكتابة بالإنجليزية (Prompt)
    prompt = f"""
    You are an expert SEO blogger and financial analyst.
    Write a highly engaging, unique, and comprehensive blog post in ENGLISH based on this news headline: "{news_title}".
    
    Requirements:
    - Length: Around 600 words.
    - Output MUST be pure HTML code only (no markdown formatting like ```html).
    - Use <h2> and <h3> for subheadings, and <p> for paragraphs.
    - Write in a professional yet captivating journalistic tone.
    - At the end of the article, create a beautiful, eye-catching CSS-styled button that says "Click Here For Exclusive Market Insights" and set its href attribute to exactly this link: {adsterra_direct_link}
    - Do not write any intro or outro, just the HTML.
    """
    
    print("🤖 AI is generating the article in English...")
    response = model.generate_content(prompt)
    article_html = response.text
    article_html = article_html.replace('```html', '').replace('```', '').strip()

    # دمج الصورة في بداية المقال إذا تم العثور عليها
    if news_image_url:
        image_html = f'<div style="text-align: center; margin-bottom: 20px;"><img src="{news_image_url}" alt="{news_title}" style="max-width: 100%; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"></div>'
        article_html = image_html + "\n" + article_html

    print("🌐 Connecting to Blogger...")
    SCOPES = ['https://www.googleapis.com/auth/blogger']
    
    if not os.path.exists('token.json'):
        print("❌ Error: token.json not found!")
        return
        
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('blogger', 'v3', credentials=creds)
    
    blog_id = os.environ.get("BLOG_ID")
    
    post_body = {
        'title': news_title,
        'content': article_html,
        'labels': ['Breaking News', 'Finance', 'Crypto']
    }
    
    print("📝 Publishing the article to Blogger...")
    request = service.posts().insert(blogId=blog_id, body=post_body, isDraft=False)
    response = request.execute()
    
    print(f"✅ Published successfully! Article URL: {response.get('url')}")

if __name__ == '__main__':
    main()
