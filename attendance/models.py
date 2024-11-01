from django.db import models


class Student(models.Model):
    student_id = models.CharField(max_length=50, unique=True)  # Unique ID for each student (RFID or manually input)
    student_name = models.CharField(max_length=100)  # Full name of the student

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ['student_name']  # Order students by their name

    def __str__(self):
        return f"{self.student_name} ({self.student_id})"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Link attendance to a student
    time_in = models.DateTimeField(null=True, blank=True)
    time_out = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Attendance Record"
        verbose_name_plural = "Attendance Records"
        ordering = ['-time_in']  # Optional: order by time_in descending

    def __str__(self):
        return f"{self.student.student_name} ({self.student.student_id}) - In: {self.time_in}, Out: {self.time_out}"

class Item(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.id})"
    
