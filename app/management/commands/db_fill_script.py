from django.db.models import ImageField
from app.models import Profile, Question, Tag, Like, Answer
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def handle(self, *args, **options):
        pic = ImageField("luke.jpg")

        usernames = set(list(User.objects.values_list('username', flat=True)))
        my_tag = Tag(name="macos")
        my_tag.save()

        for i in range(10000):
            usrname = str(i)
            if usrname not in usernames:
                n_user = User(username=usrname, password="12345_top")
                n_profile = Profile(user=n_user, name=usrname, avatar="luke.jpg")
                n_user.save()
                n_profile.save()
                for j in range(10):
                    question = Question(title="why?", text="sdasdsasdasd", rating=12, date=timezone.now(),
                                        author=n_user)
                    question.tags.add(my_tag)
                    question.save()

        for i in range(10, 1000, 1):
            usrname = str(i)
            m_user = User.objects.get(username=usrname)
            quest = Question.objects.filter(author_id=m_user.id)[:1].get()
            for j in range(3):
                answ = Answer(user=m_user, question=quest, body="asdadawdadasdas")
                answ.save()
            a_l = Like.objects.create(id_question=quest, id_user=m_user, value=True)




