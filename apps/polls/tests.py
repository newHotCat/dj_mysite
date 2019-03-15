import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

# Create your tests here.


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """未来时间"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """以前时间"""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """一天内的时间"""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        如果不存在任何问题，则会显示相应的消息。
        :return:
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '没有问题投票。')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_questions(self):
        """
        过去有pub_date的问题会显示在索引页面
        :return:
        """
        create_question(question_text='Past question.', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        将来不会显示带有pub_date的问题索引页面。
        :return:
        """
        create_question(question_text='Future question.', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "没有问题投票。")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        即使存在过去和未来的问题，也只有过去的问题显示
        :return:
        """
        create_question(question_text='Past question.', days=-30)
        create_question(question_text='Future question.', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        问题索引页面可能会显示多个问题。
        :return:
        """
        create_question(question_text='Past question 1.', days=-30)
        create_question(question_text='Past question 2.', days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        pub_tate 如果是将来的问题 页面将显示 404
        :return:
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        pub_data 如果是以前的问题， 页面将显示文本的内容
        :return:
        """
        past_question = create_question(question_text='Past question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
