from django.db import models


# Create your models here.


class Todo(models.Model):
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    completed_date = models.DateTimeField(auto_now=True, db_index=True)
    completed = models.BooleanField(default=False)
    group = models.CharField(max_length=20, default='未分类')
    text = models.CharField(max_length=200, default="none", blank=False)

    def __str__(self):
        return str(self.date)+str(self.completed)+self.text

    class Meta:
        ordering = ('-date',)


class SubTodo(models.Model):
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    completed_date = models.DateTimeField(auto_now=True, db_index=True)
    completed = models.BooleanField(default=False)
    group = models.CharField(max_length=20, default='未分类')
    text = models.CharField(max_length=200, default="none", blank=False)
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name="subTodo")

    def __str__(self):
        return str(self.date) + str(self.completed) + self.text

    class Meta:
        ordering = ('-date',)


class SSubTodo(models.Model):
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    completed_date = models.DateTimeField(auto_now=True, db_index=True)
    completed = models.BooleanField(default=False)
    group = models.CharField(max_length=20, default='未分类')
    text = models.CharField(max_length=200, default="none", blank=False)
    subtodo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name="ssubTodo")

    def __str__(self):
        return str(self.date) + str(self.completed) + self.text

    class Meta:
        ordering = ('-date',)
