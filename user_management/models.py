# from django.db import models
# from django.contrib.auth.models import User
# 
# 
# # Create your models here.
# class Role(models.Model):
#     roles = (
#         ('Super User', 'Super User'),
#         ('Admin User', 'Admin User'),
#         ('Sub User', 'Sub User'),
#     )
#     role_name = models.CharField(max_length=10, choices=roles, default='Super User')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
# 
#     def __str__(self):
#         return self.role_name
# 
#     class Meta:
#         verbose_name_plural = 'Role'
# 
# 
# class Permissions(models.Model):
#     random_password = models.BooleanField(default=True)
#     activation_email = models.BooleanField(default=True)
#     marketing_plan = models.BooleanField(default=True)
#     skip_trace = models.BooleanField(default=True)
#     list_management = models.BooleanField(default=True)
#     access_import_log = models.BooleanField(default=True)
#     access_export_log = models.BooleanField(default=True)
#     access_tag_log = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
# 
#     class Meta:
#         verbose_name_plural = 'Permission'
# 
# 
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     address = models.CharField(max_length=200, blank=True, null=True)
#     city = models.CharField(max_length=100, blank=True, null=True)
#     state = models.CharField(max_length=2, blank=True, null=True)
#     zip = models.CharField(max_length=5, blank=True, null=True)
#     email_confirmed = models.BooleanField(default=False)
#     cell_phone = models.CharField(max_length=12, blank=True, null=True, default=None)
#     landline_phone = models.CharField(max_length=12, blank=True, null=True)
#     profile_image = models.ImageField(blank=True, null=True)
#     created_by = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
#     role = models.ForeignKey(Role, null=True, on_delete=models.CASCADE)
#     permissions = models.ForeignKey(Permissions, on_delete=models.CASCADE, default=1, related_name='Permission_Object')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
# 
#     def __str__(self):
#         return self.user.username
# 
#     class Meta:
#         verbose_name_plural = 'UserProfile'
# 
# 
# class UserStripeDetail(models.Model):
#     user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=None)
#     stripe_token = models.CharField(max_length=255, blank=True, null=True, default=None)
#     subscription_id = models.CharField(max_length=255, blank=True, null=True, default=None)
#     customer_id = models.CharField(max_length=255, blank=True, null=True, default=None)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
# 
#     def __str__(self):
#         return self.user.user.username
# 
#     class Meta:
#         verbose_name_plural = 'UserStripeDetail'