from django.db import models

class Contact(models.Model):
	from_email = models.CharField(max_length=255)
	subject = models.CharField(max_length=255, blank=True)
	message = models.TextField()
	sent_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-sent_at',)
		verbose_name_plural = 'Contact Form Invoice'

	def __str__(self):
		return self.from_email