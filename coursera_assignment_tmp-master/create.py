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
delete from db_user;
delete from db_blog;
delete from db_topic;
delete from db_blog_subscribers;
delete from db_topic_likes;

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
