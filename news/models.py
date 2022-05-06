from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.

slug_length = 50


class News(models.Model):
    headline = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="news_author"
    )
    likes = models.ManyToManyField(User, related_name="news_like", blank=True)
    dislikes = models.ManyToManyField(
        User, related_name="news_dislike", blank=True)

    posted_on = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=slug_length, unique=True, blank=True)
    views = models.IntegerField(default=0, editable=False)
    thumbnail = models.ImageField(
        upload_to="news", null=True, default=None, blank=True)

    def __str__(self):
        return self.headline + " by " + str(self.author.username)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.headline)[:slug_length]
        return super(News, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("detail_post", kwargs={"pk": self.pk})

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()


class NewsComment(MPTTModel):

    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        related_name="children",
    )

    posted_on = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['posted_on']

    def __str__(self):
        return self.comment[:15] + "... by " + str(self.user.username)
