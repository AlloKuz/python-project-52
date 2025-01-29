from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)  
    description = models.TextField()  
    status = models.CharField(max_length=20, choices=[
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    ], default='TODO')  
    due_date = models.DateField(null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.title  

    class Meta:
        ordering = ['-created_at']  

