import os
import feedparser
import google.generativeai as genai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import random

def main():
    print("🚀 بدء تشغيل السكربت...")

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ خطأ: لم يتم العثور على مفتاح GEMINI_API_KEY")
        return
        
    genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')
    # قمنا بإضافة 3 مصادر أخبار قوية لضمان وجود أخبار دائماً
    rss_urls = [
        "https://arabic.cnn.com/api/v1/rss/business/rss.xml",
        "https://www.aljazeera.net/api/v1/rss/economy/rss.xml",
        "https://ar.cointelegraph.com/rss"
    ]
    
    news_title = ""
    # السكربت سيجرب الروابط واحداً تلو الآخر حتى يجد خبراً
    for url in rss_urls:
        feed = feedparser.parse(url)
        if feed.entries:
            news_title = feed.entries[0].title
            break
            
    if not news_title:
        print("❌ لم يتم العثور على أي أخبار في جميع المصادر اليوم.")
        return
        
    print(f"📰 تم التقاط خبر جديد بعنوان: {news_title}")

    # ====================================================
    # 🔴 هام: رابط Adsterra المباشر الخاص بك 
    # ====================================================
    adsterra_direct_link = "https://www.profitablecpmratenetwork.com/zu9q64fcp?key=ae8877384966f5230b597373dfdcd7b2"

    prompt = f"""
    أنت مدون خبير في السيو (SEO) والاقتصاد والتقنية.
    اكتب مقالاً حصرياً وشاملاً باللغة العربية بناءً على هذا الخبر: "{news_title}".
    
    شروط المقال:
    - طول المقال 500 كلمة.
    - استخدم تنسيق HTML فقط (استخدم وسوم <h2> و <h3> للعناوين الفرعية، و <p> للفقرات).
    - لا تكتب أي مقدمات، أعطني كود HTML مباشرة.
    - في منتصف المقال وفي نهايته، قم بإنشاء زر أنيق باستخدام HTML و CSS مكتوب عليه "اضغط هنا لمتابعة أحدث التوصيات الحصرية" واجعل الرابط الخاص به هو هذا: {adsterra_direct_link}
    """
    
    print("🤖 جاري كتابة المقال بالذكاء الاصطناعي...")
    response = model.generate_content(prompt)
    article_html = response.text
    article_html = article_html.replace('```html', '').replace('```', '').strip()

    print("🌐 جاري الاتصال بمدونة بلوجر...")
    SCOPES = ['https://www.googleapis.com/auth/blogger']
    
    if not os.path.exists('token.json'):
        print("❌ خطأ: ملف token.json غير موجود!")
        return
        
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('blogger', 'v3', credentials=creds)
    
    blog_id = os.environ.get("BLOG_ID")
    
    post_body = {
        'title': news_title,
        'content': article_html,
        'labels': ['أخبار عاجلة', 'اقتصاد']
    }
    
    print("📝 جاري إرسال المقال إلى بلوجر...")
    request = service.posts().insert(blogId=blog_id, body=post_body, isDraft=False)
    response = request.execute()
    
    print(f"✅ تم النشر بنجاح! رابط المقال: {response.get('url')}")

if __name__ == '__main__':
    main()
