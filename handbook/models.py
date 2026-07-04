from django.db import models


class ChatbotFAQ(models.Model):
    question = models.CharField(max_length=255, verbose_name='問題')
    answer = models.TextField(verbose_name='答案')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question


class SalaryRecord(models.Model):
    lesson_label = models.CharField(max_length=50, verbose_name='課程標籤')
    lesson_count = models.FloatField(verbose_name='堂數')
    question_count = models.FloatField(verbose_name='解題數量')
    preparation_fee = models.FloatField(verbose_name='準備費')
    image_fee = models.FloatField(verbose_name='形象費')
    material_fee = models.FloatField(verbose_name='教材加給')
    duration_fee = models.FloatField(verbose_name='授課基礎費')
    question_fee = models.FloatField(verbose_name='解題費用')
    total_salary = models.FloatField(verbose_name='總薪資')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='紀錄時間')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '薪資紀錄'
        verbose_name_plural = '薪資紀錄'

    def __str__(self):
        return f"{self.created_at:%Y-%m-%d} {self.lesson_label} {self.total_salary}"