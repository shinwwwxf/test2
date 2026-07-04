import uuid
from datetime import date

from django.db.models import Sum
from django.shortcuts import render
from .models import ChatbotFAQ, SalaryRecord

RATE_TABLE = {
    "國小解題教室": {"base": 10, "preparation": 115, "image": 35, "material": 0},
    "國中解題教室": {"base": 15, "preparation": 140, "image": 35, "material": 0},
    "高中解題教室": {"base": 20, "preparation": 165, "image": 35, "material": 0},
}


def home(request):
    return render(request, "home.html")


def salary_calculator(request):
    result = None
    if request.method == "POST":
        try:
            lesson_label = request.POST.get("lesson_label", "")
            lesson_count = float(request.POST.get("lesson_count", 0))
            question_count = float(request.POST.get("question_count", 0))

            rate = RATE_TABLE.get(lesson_label)
            if not rate:
                result = {"error": "請選擇有效的課程標籤。"}
            else:
                preparation_fee = rate["preparation"]
                image_fee = rate["image"]
                material_fee = rate["material"]
                base_fee = rate["base"]
                # 每堂固定 30 分鐘,所以堂數直接乘上單堂的準備費/形象費/教材加給
                duration_fee = round((preparation_fee + image_fee + material_fee) * lesson_count, 2)
                question_fee = round(question_count * base_fee, 2)
                total_salary = round(duration_fee + question_fee, 2)

                # 每次計算都存一筆上課紀錄,之後才能累加整個月的堂數與薪資
                SalaryRecord.objects.create(
                    lesson_label=lesson_label,
                    lesson_count=lesson_count,
                    question_count=question_count,
                    preparation_fee=preparation_fee,
                    image_fee=image_fee,
                    material_fee=material_fee,
                    duration_fee=duration_fee,
                    question_fee=question_fee,
                    total_salary=total_salary,
                )

                result = {
                    "lesson_label": lesson_label,
                    "lesson_count": lesson_count,
                    "question_count": question_count,
                    "preparation_fee": preparation_fee,
                    "image_fee": image_fee,
                    "material_fee": material_fee,
                    "duration_fee": duration_fee,
                    "question_fee": question_fee,
                    "total_salary": total_salary,
                }
        except ValueError:
            result = {"error": "請輸入有效的數字。"}

    # 統計「本月」所有紀錄的堂數總和與薪資總和
    today = date.today()
    monthly_records = SalaryRecord.objects.filter(
        created_at__year=today.year,
        created_at__month=today.month,
    )
    monthly_summary = monthly_records.aggregate(
        total_lesson_count=Sum("lesson_count"),
        total_salary=Sum("total_salary"),
    )

    return render(
        request,
        "salary_calculator.html",
        {
            "result": result,
            "monthly_records": monthly_records,
            "monthly_lesson_count": monthly_summary["total_lesson_count"] or 0,
            "monthly_total_salary": monthly_summary["total_salary"] or 0,
            "current_month": today.strftime("%Y年%m月"),
        },
    )


def salary_chatbot(request):
    return render_chatbot(request, "salary", "報酬問題")


def absence_chatbot(request):
    return render_chatbot(request, "absence", "無法到課問題")


def entry_chatbot(request):
    return render_chatbot(request, "entry", "入職申請問題")


def render_chatbot(request, theme, title):
    chat_id = request.GET.get("chat_id") or request.POST.get("chat_id") or str(uuid.uuid4())
    session_key = f"chat_messages_{theme}_{chat_id}"
    messages = request.session.get(session_key, [])

    if request.method == "POST":
        question = request.POST.get("question", "").strip()
        if question:
            messages.append({"role": "user", "content": question})
            messages.append({"role": "assistant", "content": get_answer(question, theme)})
            request.session[session_key] = messages
            request.session.modified = True

    history = []
    history_keys = [key for key in request.session.keys() if key.startswith(f"chat_messages_{theme}_")]
    for index, key in enumerate(history_keys, start=1):
        if key == session_key:
            history.append({"chat_id": chat_id, "label": f"對話 {index}"})
        else:
            history.append({"chat_id": key.replace(f"chat_messages_{theme}_", ""), "label": f"對話 {index}"})

    if not history:
        history.append({"chat_id": chat_id, "label": "對話 1"})

    return render(
        request,
        "chatbot.html",
        {
            "messages": messages,
            "title": title,
            "theme": theme,
            "chat_id": chat_id,
            "history": history,
            "theme_label": title,
            "new_chat_id": str(uuid.uuid4()),
        },
    )


def get_answer(question, theme):
    q = question.lower().strip()

    # 1. 從資料庫抓出所有的問答資料
    all_faqs = ChatbotFAQ.objects.all()

    # 2. 透過迴圈進行「雙向比對」
    for faq in all_faqs:
        db_question = faq.question.lower()

        # 情況 A：使用者輸入短字詞（例如「環境」），看有沒有包含在資料庫的長問題中
        if q in db_question:
            return faq.answer

        # 情況 B：使用者輸入長句子（例如「我明天想請假」），看資料庫設定的關鍵字有沒有在句子裡
        # 將資料庫裡用逗號分隔的關鍵字切開來逐一比對
        keywords = db_question.replace('、', ',').split(',')
        for kw in keywords:
            kw = kw.strip()
            if kw and kw in q:
                return faq.answer

    # 3. 如果資料庫真的都找不到匹配的答案，才退回到各主題的「預設引導訊息」
    if theme == "salary":
        return "這是報酬專區，您可以詢問薪水、待遇、津貼或報酬相關問題。"
    elif theme == "absence":
        return "這是請假與缺課專區，您可以詢問無法到課、請假或補課相關問題。"
    elif theme == "entry":
        return "這是入職申請專區，您可以詢問報到、申請文件或入職流程相關問題。"

    return "請直接輸入與此主題相關的問題，或嘗試輸入更簡短的關鍵字（例如：「申請」、「環境」）。"