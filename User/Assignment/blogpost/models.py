from django.db import models
from assignment.models import NewUser

class BlogPost(models.Model):
    title=models.CharField(max_length=30)
    description=models.TextField()
    published_date=models.DateTimeField(auto_now_add=True)
    is_deleted=models.BooleanField(default=False)
    author=models.ForeignKey(NewUser,null=True,on_delete=models.CASCADE,related_name='blog_post')

    def __str__(self):
        return self.title
    
    def delete(self,hard_delete=False):
        if hard_delete:
            super().delete()
        else:
            self.is_deleted=True
            self.save()
    def restore(self):
        self.is_deleted=False
        self.save()