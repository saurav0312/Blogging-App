from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

class Post(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    image = models.ImageField(default='default.jpg', upload_to='post_pics')
    date_posted=models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    like=models.SmallIntegerField(default=0)
    liked_by=models.ManyToManyField(User,related_name='liked_by',blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
          return reverse('post-detail',kwargs={'pk':self.pk})

    def save(self,**kwargs):
        super().save()
        img=Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


