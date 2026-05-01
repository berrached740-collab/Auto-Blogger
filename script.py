import os
import feedparser
import google.generativeai as genai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def main():
    print("🚀 بدء تشغيل السكربت...")

    # 1. التحقق من مفتاح الذكاء الاصطناعي (Gemini)
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ خطأ: لم يتم العثور على مفتاح GEMINI_API_KEY")
        return
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro')

    # 2. جلب أحدث خبر من RSS (كمثال: أخبار العملات الرقمية التي تتميز بـ CPM عالي)
    rss_url = "https://ar.cointelegraph.com/rss"
    feed = feedparser.parse(rss_url)
    
    if not feed.entries:
        print("❌ لم يتم العثور على أخبار في الرابط.")
        return
        
    latest_entry = feed.entries[0]
    news_title = latest_entry.title
    
    print(f"📰 تم التقاط خبر جديد بعنوان: {news_title}")

    # ====================================================
    # 🔴 هام: ضع رابط Adsterra المباشر (Smartlink) الخاص بك هنا
    # ====================================================
    adsterra_direct_link = "https://www.profitablecpmratenetwork.com/zu9q64fcp?key=ae8877384966f5230b597373dfdcd7b2"

    # 3. توجيه الأوامر (Prompt) للذكاء الاصطناعي
    prompt = f"""
    أنت مدون خبير في السيو (SEO) ومجال العملات الرقمية والتقنية.
    اكتب مقالاً حصرياً وشاملاً باللغة العربية بناءً على هذا الخبر: "{news_title}".
    
    شروط المقال:
    - طول المقال بين 600 إلى 800 كلمة.
    - استخدم تنسيق HTML فقط (استخدم وسوم <h2> و <h3> للعناوين الفرعية، و <p> للفقرات، و <ul> للقوائم).
    - لا تكتب "إليك المقال" أو أي مقدمات، أعطني كود HTML مباشرة لكي أنسخه في مدونتي.
    - اكتب بأسلوب صحفي جذاب يشد القارئ.
    - في منتصف المقال وفي نهايته، قم بإنشاء زر أنيق باستخدام HTML و CSS مكتوب عليه "اضغط هنا لمتابعة أحدث التوصيات الحصرية" واجعل الرابط الخاص به هو هذا: {adsterra_direct_link}
    """
    
    print("🤖 جاري كتابة المقال بالذكاء الاصطناعي...")
    response = model.generate_content(prompt)
    article_html = response.text
    
    # تنظيف الكود (إزالة أي علامات غريبة قد يضيفها الذكاء الاصطناعي)
    article_html = article_html.replace('```html', '').replace('```', '').strip()

    # 4. الاتصال بمدونة بلوجر ونشر المقال
    print("🌐 جاري الاتصال بمدونة بلوجر...")
    SCOPES = ['https://www.googleapis.com/auth/blogger']
    
    if not os.path.exists('token.json'):
        print("❌ خطأ: ملف token.json غير موجود!")
        return
        
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('blogger', 'v3', credentials=creds)
    
    blog_id = os.environ.get("BLOG_ID")
    if not blog_id:
        print("❌ خطأ: لم يتم العثور على BLOG_ID")
        return
    
    post_body = {
        'title': news_title,
        'content': article_html,
        'labels': ['أخبار عاجلة', 'عملات رقمية'] # تصنيفات المقال
    }
    
    # النشر في المدونة (isDraft=False تعني نشر فوري للجمهور)
    print("📝 جاري إرسال المقال إلى بلوجر...")
    request = service.posts().insert(blogId=blog_id, body=post_body, isDraft=False)
    response = request.execute()
    
    print(f"✅ تم النشر بنجاح! رابط المقال: {response.get('url')}")

if __name__ == '__main__':
    main()
