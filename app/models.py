from django.db import models
from django.contrib.auth.models import User
from app.managers import UserManager, QuestionManager, TagManager, AnswerManager, LikeQManager
from django.shortcuts import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    avatar = models.ImageField(null=True, blank=True, verbose_name=u"аватар", upload_to='static/images/')
    name = models.CharField(max_length=40)
    objects = UserManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Авторы"
        verbose_name_plural = "Авторы"


class Tag(models.Model):
    name = models.CharField(max_length=40,default="os")
    objects = TagManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    tags = models.ManyToManyField(Tag)
    rating = models.IntegerField(default=0,verbose_name="rating")
    date = models.DateField(verbose_name="date added", auto_now_add=True)

    objects = QuestionManager()

    def get_absolute_url(self):
        return "/question/%i/" % self.pk
        # return reverse('question_answers', kwargs={'pk':})

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"



class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    question = models.ForeignKey(Question, on_delete=models.CASCADE,default=None)
    body = models.TextField()
    is_correct = models.BooleanField(verbose_name='верный', default=False)
    rating_num = models.IntegerField(verbose_name='рейтинг', default=0)
    added_on = models.DateTimeField(blank=True, auto_now_add=True, verbose_name='дата и время добавления')
    objects=AnswerManager()



class Like(models.Model):
    id_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, null=False, verbose_name='id', on_delete=models.CASCADE)
    value = models.BooleanField(default=False)

    objects=LikeQManager()

    class Meta:
        unique_together = ('id_question', 'id_user')

    def __str__(self):
        return str(self.id_question)


class Answer_Like(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=False, verbose_name='id', on_delete=models.CASCADE)
    value = models.BooleanField(default=False)

    class Meta:
        unique_together = ('question', 'user')
