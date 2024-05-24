from django.db import models
from django.utils import timezone
import string
import random

class Context(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, max_length=6, blank=True)

    def __str__(self):
        return timezone.localtime(self.created_at).strftime('%d/%m/%Y %H:%M:%S') + ' - ' + self.text[:35]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
            while Context.objects.filter(slug=self.slug).exists():
                self.slug = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
            
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Context'
        verbose_name_plural = 'Contexts'
        