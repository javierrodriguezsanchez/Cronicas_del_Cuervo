from django.db import models

class WeeklyJournal(models.Model):
    file = models.FileField(upload_to='journals/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Journal uploaded on {self.uploaded_at.date()}"

