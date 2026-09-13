class Student(models.Model):
    name = models.CharField()
    age = models.IntegerField()

    student = Student.object.all()