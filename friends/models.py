from django.db import models
from dashboard.models import Login_info_new_p


class friend_list(models.Model):
    user_id = models.ForeignKey(Login_info_new_p, on_delete=models.CASCADE, related_name="user")
    friend_id = models.ForeignKey(Login_info_new_p, on_delete=models.CASCADE, related_name="friend")
    create_at = models.DateTimeField(auto_now_add=True)


class friend_request(models.Model):
    sender_id = models.ForeignKey(Login_info_new_p, on_delete=models.CASCADE, related_name="sent_requests")
    receiver_id = models.ForeignKey(Login_info_new_p, on_delete=models.CASCADE, related_name="received_requests")
    status = models.CharField(
        max_length=10,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ]
    )
    create_at = models.DateTimeField(auto_now_add=True)
