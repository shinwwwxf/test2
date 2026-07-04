from django.test import TestCase
from django.urls import reverse


class SalaryCalculatorTests(TestCase):
    def test_calculates_salary_from_label_and_questions(self):
        response = self.client.post(
            reverse("salary_calculator"),
            {
                "lesson_label": "高中解題教室",
                "duration_minutes": "30",
                "question_count": "5",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "總薪資")
        self.assertContains(response, "300")

    def test_chatbot_keeps_separate_histories_for_different_chat_ids(self):
        first_response = self.client.post(
            reverse("salary_chatbot"),
            {"question": "請問薪水怎麼算", "chat_id": "chat-a"},
        )
        second_response = self.client.post(
            reverse("salary_chatbot"),
            {"question": "請問報酬內容", "chat_id": "chat-b"},
        )
        first_view = self.client.get(reverse("salary_chatbot") + "?chat_id=chat-a")

        self.assertContains(first_response, "請問薪水怎麼算")
        self.assertContains(second_response, "請問報酬內容")
        self.assertContains(first_view, "請問薪水怎麼算")
        self.assertNotContains(first_view, "請問報酬內容")

    def test_chatbot_shows_previous_conversation_list(self):
        response = self.client.post(
            reverse("salary_chatbot"),
            {"question": "請問薪水怎麼算", "chat_id": "chat-history"},
        )

        self.assertContains(response, "請問薪水怎麼算")
        self.assertContains(response, "新增對話")
        self.assertContains(response, "對話")
