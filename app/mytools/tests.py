from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Context
import datetime

class ContextDetailViewTests(TestCase):

    def setUp(self):
        self.context = Context.objects.create(
            text='This is a test context',
            expires_at=timezone.now() + datetime.timedelta(days=1),  # valido
            is_active=True
        )
        self.expired_context = Context.objects.create(
            text='This is an expired context',
            expires_at=timezone.now() - datetime.timedelta(days=1),  # expirado a 1 dia atras
            is_active=True
        )
        self.inactive_context = Context.objects.create(
            text='This is an inactive context',
            expires_at=timezone.now() - datetime.timedelta(days=1),
            is_active=False
        )

    def test_context_detail_active_context(self):
        url = reverse('context_detail', kwargs={'slug': self.context.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.context.text)
        self.assertNotContains(response, 'error')

    def test_context_detail_expired_context(self):
        url = reverse('context_detail', kwargs={'slug': self.expired_context.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.expired_context.refresh_from_db()
        self.assertFalse(self.expired_context.is_active)

    def test_context_detail_inactive_context(self):
        url = reverse('context_detail', kwargs={'slug': self.inactive_context.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_context_detail_nonexistent_context(self):
        url = reverse('context_detail', kwargs={'slug': 'nonexistent'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)