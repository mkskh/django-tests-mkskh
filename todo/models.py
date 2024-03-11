from django.db import models


# class User(models.Model):
#     login = models.CharField(max_length=20)
#     password = models.CharField(max_length=20)


# credentials = [
#     {
#         "login": "mks_kh",
#         "password": "test1234"
#     },
# ]


todos = [
    {
        "text": "Start the repository",
        "topic": "Course Project",
        "status": "done"
    },
    {
        "text": "Set up Django",
        "topic": "Course Project",
        "status": "done"
    },
    {
        "text": "Read more about URLconf",
        "topic": "Lectures",
        "status": "done"
    },
    {
        "text": "Fix the cabinet",
        "topic": "Personal",
        "status": "done"
    },
    {
        "text": "Create forms",
        "topic": "Course Project",
        "status": "pending"
    },
]


# class ToDoList(models.Model):
#     title = models.CharField(max_length=100)
#     text = models.TextField()
#     status = models.BooleanField(default=False)