from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Blog

# Triggered before saving a Blog instance
@receiver(pre_save, sender=Blog)
def before_blog_save(sender, instance, **kwargs):
    print(f"Pre-save signal triggered for {instance.title}")

# Triggered after saving a Blog instance
@receiver(post_save, sender=Blog)
def after_blog_save(sender, instance, created, **kwargs):
    if created:
        print(f"Post-save signal triggered for {instance.title} (created)")
    else:
        print(f"Post-save signal triggered for {instance.title} (updated)")