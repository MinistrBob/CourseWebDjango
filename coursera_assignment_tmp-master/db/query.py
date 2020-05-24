from datetime import datetime

from django.db.models import Q, Count, Avg
from pytz import UTC

from db.models import User, Blog, Topic


def create():
    """
    Создать пользователя first_name = u1, last_name = u1.
    Создать пользователя first_name = u2, last_name = u2.
    Создать пользователя first_name = u3, last_name = u3.
    Создать блог title = blog1, author = u1.
    Создать блог title = blog2, author = u1.
    Подписать пользователей u1 u2 на blog1, u2 на blog2.
    Создать топик title = topic1, blog = blog1, author = u1.
    Создать топик title = topic2_content, blog = blog1, author = u3, created = 2017-01-01.
    Лайкнуть topic1 пользователями u1, u2, u3.
    :return:
    """
    u1 = User(first_name="u1", last_name="u1")
    u1.save()
    u2 = User(first_name="u2", last_name="u2")
    u2.save()
    u3 = User(first_name="u3", last_name="u3")
    u3.save()
    blog1 = Blog(title="blog1", author=u1)
    blog1.save()
    blog2 = Blog(title="blog2", author=u1)
    blog2.save()
    blog1.subscribers.add(u1, u2)
    blog1.save()
    blog2.subscribers.add(u2)
    blog2.save()
    topic1 = Topic(title="topic1", blog=blog1, author=u1)
    topic1.save()
    topic2 = Topic(title="topic2_content", blog=blog1, author=u3, created=datetime(2017, 1, 1))
    topic2.save()
    topic1.likes.add(u1, u2, u3)
    topic1.save()


def edit_all():
    """
	Поменять first_name на uu1 у всех пользователей (функция edit_all)
	"""
    User.objects.all().update(first_name="uu1")


def edit_u1_u2():
    """Поменять first_name на uu1 у пользователей, у которых first_name u1 или u2 (функция edit_u1_u2)"""
    User.objects.filter(Q(first_name='u1') | Q(first_name='u2')).update(first_name="uu1")


def delete_u1():
    """удалить пользователя с first_name u1 (функция delete_u1)"""
    u1 = User.objects.get(first_name="u1")
    u1.delete()


def unsubscribe_u2_from_blogs():
    """отписать пользователя с first_name u2 от блогов (функция unsubscribe_u2_from_blogs)."""
    u2 = User.objects.get(first_name="u2")
    u2.subscriptions.clear()


def get_topic_created_grated():
    """Найти топики у которых дата создания больше 2018-01-01 (функция get_topic_created_grated)."""
    return Topic.objects.filter(created__gt='2018-01-01')


def get_topic_title_ended():
    """Найти топик у которого title заканчивается на content (функция get_topic_title_ended)."""
    return Topic.objects.filter(title__endswith='content')


def get_user_with_limit():
    """Получить 2х первых пользователей (сортировка в обратном порядке по id) (функция get_user_with_limit)"""
    return User.objects.all().order_by('-id')[0:2]


def get_topic_count():
    """Получить количество топиков в каждом блоге, назвать поле topic_count, отсортировать по topic_count по возрастанию (функция get_topic_count)"""
    return Blog.objects.annotate(topic_count=Count('topic')).order_by('topic_count')


def get_avg_topic_count():
    """Получить среднее количество топиков в блоге (функция get_avg_topic_count)."""
    return Blog.objects.annotate(topic_count=Count('topic')).aggregate(avg=Avg('topic_count'))


def get_blog_that_have_more_than_one_topic():
    """Найти блоги, в которых топиков больше одного (функция get_blog_that_have_more_than_one_topic)."""
    return Blog.objects.annotate(topic_count=Count('topic')).filter(topic_count__gt=1)


def get_topic_by_u1():
    """Получить все топики автора с first_name u1 (функция get_topic_by_u1)."""
    return Topic.objects.filter(author__first_name='u1')


def get_user_that_dont_have_blog():
    """Найти пользователей, у которых нет блогов, отсортировать по возрастанию id (функция get_user_that_dont_have_blog)."""
    return User.objects.filter(blog__author_id__isnull=True)


def get_topic_that_like_all_users():
    """Найти топик, который лайкнули все пользователи (функция get_topic_that_like_all_users)."""
    m = User.objects.count()
    q = Topic.objects.annotate(like=Count('likes'))
    return q.filter(like=m)
    # for t in q:
    #     if t.likes__count == m:
    #         return t


def get_topic_that_dont_have_like():
    """Найти топики, у которых нет лайков (функция get_topic_that_dont_have_like)."""
    return Topic.objects.filter(likes__isnull=True)
