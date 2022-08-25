from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Snack


class SnackTests(TestCase):
  def setUp(self):
    self.user = get_user_model().objects.create_user(
      username="tester", email="tester@email.com", password="pass"
    )

    self.snack = Snack.objects.create(
      title="chips", description="crunchy", purchaser=self.user,
    )

  def test_string_representation(self):
    self.assertEqual(str(self.snack), "chips")

  
  def test_snack_content(self):
    self.assertEqual(str(self.snack.title), "chips")
    self.assertEqual(str(self.snack.purchaser), "tester")
    self.assertEqual(str(self.snack.description), "crunchy")

  
  def test_snack_list(self):
    response = self.client.get(reverse("snack_list"))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "chips")
    self.assertTemplateUsed(response, "snack_list.html")

  def test_snack_detail_view(self):
        response = self.client.get(reverse("snack_detail", args="1"))
        no_response = self.client.get("/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "chips")
        self.assertTemplateUsed(response, "snack_detail.html")

  def test_snack_create_view(self):
      response = self.client.post(
          reverse("snack_create"),
          {
              "title": "apple",
              "description": "One a day keeps the doctor away",
              "purchaser": self.user.id,
          }, follow=True
      )

      self.assertRedirects(response, reverse("snack_detail", args="2"))
      self.assertContains(response, "One a day keeps the doctor away")

  def test_snack_update_view_redirect(self):
      response = self.client.post(
          reverse("snack_update", args="1"),
          {"title": "Updated name", "description": "low on calories", "purchaser": self.user.id}
      )

      self.assertRedirects(response, reverse("snack_detail", args="1"))
      

  def test_snack_delete_view(self):
      response = self.client.get(reverse("snack_delete", args="1"))
      self.assertEqual(response.status_code, 200)