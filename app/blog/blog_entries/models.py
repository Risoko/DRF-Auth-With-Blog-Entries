from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator

from blog_auth.models import User


class Article(models.Model):
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    pub_date = models.DateField(
        verbose_name=_('publish date'),
        help_text=_('Enter the publication date of the article.'),
        default=now
    )
    like = models.SmallIntegerField(
        verbose_name=_('you like it'),
        default=0
    )
    dislike = models.SmallIntegerField(
        verbose_name=_('you dislike it'),
        default=0
    )
    title = models.CharField(
        verbose_name=_('title'),
        max_length=300,
        help_text=_('Enter title.'),
        validators=[MinLengthValidator(limit_value=10)]
    )
    entry = models.TextField(
        verbose_name=_('blog entry'),
        help_text=_('Your blog entry'),
        validators=[MinLengthValidator(limit_value=200)]
    )

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        ordering = ['-pub_date']
    
    def check_the_owner(self, author):
        return self.author.user_authenticate_data.username == author.username or author.is_superuser       

    def __str__(self):
        return self.title
