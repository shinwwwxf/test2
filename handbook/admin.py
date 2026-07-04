from django.contrib import admin
from .models import ChatbotFAQ, SalaryRecord


@admin.register(ChatbotFAQ)
class ChatbotFAQAdmin(admin.ModelAdmin):
    list_display = ("question", "created_at")


@admin.register(SalaryRecord)
class SalaryRecordAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "lesson_label",
        "lesson_count",
        "question_count",
        "total_salary",
    )
    list_filter = ("lesson_label", "created_at")