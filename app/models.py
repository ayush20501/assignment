from django.db import models


class MarkSheet(models.Model):
    student_name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=10, unique=True)
    subject1 = models.CharField(max_length=50)
    subject2 = models.CharField(max_length=50)
    subject3 = models.CharField(max_length=50)
    subject4 = models.CharField(max_length=50)
    subject5 = models.CharField(max_length=50)
    subject1_score = models.IntegerField()
    subject2_score = models.IntegerField()
    subject3_score = models.IntegerField()
    subject4_score = models.IntegerField()
    subject5_score = models.IntegerField()
    image = models.ImageField(upload_to='student_images/')
    student_class = models.IntegerField(choices=[(i, i) for i in range(1, 13)])
    total_marks = models.IntegerField(blank=True, null=True)

    def calculate_total_marks(self):
        return (
            self.subject1_score + self.subject2_score + self.subject3_score + self.subject4_score + self.subject5_score)

    def save(self):
        self.total_marks = self.calculate_total_marks()
        super().save()

    def __str__(self):
        return self.student_name