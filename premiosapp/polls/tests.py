import datetime
from email.policy import default
from pyexpat import model

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

# Instances creator
def create_question(question_text,minutes=0):
    """Creates a question with the given "question _text", and published at
    the given number of offset minutes since now (negative for questions 
    published in the past, positive for questions yet to be pubished).

    Args:
        question_text (str): Question itself
        minutes (int): offset minutes
    """
    time = timezone.now() + datetime.timedelta(minutes=minutes)
    return Question.objects.create(question_text=question_text, pub_date=time)

#Test models and views

# Model test.
class QuestionModelTest(TestCase):
    def setUp(self):
        self.question = Question(question_text="Who is the best person?")

    def test_was_published_recently_with_future_question(self):
        """was_published_recently returns False for questions whose pub_date is in the future
        """
        time = timezone.now() + datetime.timedelta(minutes=1)
        self.question.pub_date=time
        #future_question= Question(question_text="Who is the best person?", pub_date= time)
        #self.assertIs(future_question.was_published_recently(), False)
        self.assertFalse(self.question.was_published_recently())
    
    def test_was_published_recently_with_now_question(self):
        """was_published_recently returns True for questions whose pub_date is in the present
        """
        time = timezone.now()
        self.question.pub_date=time
        #present_question= Question(question_text="Who is the best person?", pub_date= time)
        #self.assertIs(present_question.was_published_recently(), True)
        self.assertTrue(self.question.was_published_recently())
    
    def test_was_published_recently_with_past_question(self):
        """was_published_recently returns False for questions whose pub_date is in the past
        """
        time = timezone.now()- datetime.timedelta(days=1, seconds=1)
        self.question.pub_date=time
        #past_question= Question(question_text="Who is the best person?", pub_date= time)
        #self.assertIs(past_question.was_published_recently(), False)
        self.assertFalse(self.question.was_published_recently())



class QuestionIndexViewTest(TestCase):
    def test_no_question(self):
        """If no question exist, an appropiate message is displayed
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])    

    def test_dont_display_future_questions(self):
        """If a future question exist, it must not be displayed
        """
        future_question=create_question(question_text="Future question?", minutes=1)
        response = self.client.get(reverse("polls:index"))
        self.assertNotIn(future_question, response.context["latest_question_list"])
        
    def test_display_present_questions(self):
        """Questions published now or in the past must be displayed.
        """
        present_question=create_question(question_text="Past question?", minutes=0)
        response = self.client.get(reverse("polls:index"))
        self.assertIn(present_question, response.context["latest_question_list"])
        
    def test_future_and_past_question_simultaneously(self):
        present_question=create_question(question_text="Past question?", minutes=0)
        future_question=create_question(question_text="Future question?", minutes=1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual([present_question],response.context["latest_question_list"]) 

    def test_two_past_question(self):
        present_question=create_question(question_text="Past question?", minutes=0)
        present2_question=create_question(question_text="past2 question?", minutes=-1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual([present_question,present2_question],response.context["latest_question_list"])

    def test_two_future_question(self):
        future_question=create_question(question_text="Past question?", minutes=1)
        future2_question=create_question(question_text="past2 question?", minutes=2)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual([],response.context["latest_question_list"])


class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        future_question=create_question(question_text="Future question?", minutes=1)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)
    
    def test_past_question(self):
        past_question=create_question(question_text="Past question?", minutes=0)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response,past_question.question_text)


class ResultsViewTest(TestCase):
    def test_no_choices_question(self):
        question=create_question(question_text="No choices question?", minutes=0)
        url = reverse("polls:results", args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404) 

    def test_less_tha_two_choices_question(self):
        question=create_question(question_text="No choices question?", minutes=0)
        question.choice_set.create(choice_text="choice_text", votes=0)
        url = reverse("polls:results", args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404) 

    def test_two_choices_question(self):
        question=create_question(question_text="No choices question?", minutes=0)
        question.choice_set.create(choice_text="choice_text", votes=0)
        question.choice_set.create(choice_text="choice_text2", votes=0)
        url = reverse("polls:results", args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,200) 