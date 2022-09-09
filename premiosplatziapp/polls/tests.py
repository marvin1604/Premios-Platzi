import datetime
from http import client
from urllib import response

from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse 
from .models import Question
#test models
class QuestionModelsTests(TestCase):
    
    def test_was_published_recently_width_future_questions(self):
        """was_published_recently return False for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="quien es el mejor course director de platzi?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_published_recently_with_past_questions(self):
        """was_published_recently() must return Flase for questions whose pub_date is more than 1 day in the past"""
        time = timezone.now() - datetime.timedelta(days=30)
        past_question = Question(question_text="¿Quien es el mejor Course Direct de Platzi?",pub_date=time)
        self.assertIs(past_question.was_published_recently(),False)

    def test_was_published_recently_with_present_questions(self):
        """was_published_recently() must return True for questions whose pub_date is actual"""
        time = timezone.now()
        present_question = Question(question_text="¿Quien es el mejor Course Direct de Platzi?",pub_date=time)
        self.assertIs(present_question.was_published_recently(),True)
    
    


def create_question(question_text, days):
    """ 
    Create a question with the given "question_text", and published the given number
    of days offset to now(negative for question published in the past, positive for 
    question that have yet to be published)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time) 

#test Views
class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """If no question exist, an appropiate is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question(self):
        """
        Question with a pub_date in the future aren´t displayed on the index page """
        create_question("Future Question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Question with a pub_date in the past are displayed on the index page
        """
        question = create_question("Future Question", days=-10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])

    def test_future_question_and_past_question(self):
        """"
        even if both and future question exist, only past question are displayed
        """
        past_question = create_question(question_text="Past question", days= -30)
        future_question = create_question(question_text="Future question", days= 30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question]
        )

    def test_two_past_question(self):
        """ The questions index page may display multiple question"""
        past_question1 = create_question(question_text="Past question 1", days= -30)
        past_question2 = create_question(question_text="Past question 2", days= -40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question1, past_question2]
        )
        
    def test_two_future_question(self):
        """ The questions index page may display multiple question"""
        future_question1 = create_question(question_text="Future question1", days= 30)
        future_question2 = create_question(question_text="Future question2", days= 40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            []
        )

class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future returns a 404 
        error not found
        """
        future_question = create_question(question_text="Future question", days= 30)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


    def test_past_question(self):
        """
        The detail view a question with a pub_date in the past displays the question´s text
        """
        past_question = create_question(question_text="Past question", days= -30)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
