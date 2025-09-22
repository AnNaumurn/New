from django.db import models
from dashboard.models import Login_info_new_p

class Comment(models.Model):
    author = models.ForeignKey(Login_info_new_p, on_delete=models.CASCADE, related_name="comments_made")
    profile_owner = models.ForeignKey(Login_info_new_p, on_delete=models.CASCADE, related_name="comments_received")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author.fname} → {self.profile_owner.fname}: {self.text[:20]}"
