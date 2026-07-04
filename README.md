# 教師手冊系統 (Teacher Handbook System)

一個 Django 專案,提供:

- **薪資計算器**:依課程標籤(國小/國中/高中解題教室)、授課時長、解題數量估算教師報酬
- **三個主題聊天機器人**:報酬問題、無法到課問題、入職申請問題,會依 `ChatbotFAQ` 資料表比對關鍵字回答,找不到才顯示預設引導訊息

## 專案結構

```
mysite/            # Django 專案設定 (settings.py, urls.py)
handbook/          # 主要 app:models, views, urls, templates
static/styles.css  # 樣式表
```

## 快速開始

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # 選擇性,用來到 /admin/ 新增 FAQ 資料
python manage.py runserver
```

開啟 http://127.0.0.1:8000/ 即可看到系統首頁。

## 補充 FAQ 資料

聊天機器人的回答來自 `ChatbotFAQ` 資料表(問題／答案),可以到 `/admin/` 後台新增,
或用 Django shell:

```python
from handbook.models import ChatbotFAQ
ChatbotFAQ.objects.create(question="薪水,待遇", answer="教師報酬會於每月 5 號發放。")
```
