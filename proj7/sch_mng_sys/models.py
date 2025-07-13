from django.db import models

# Subject choices per class
CLASS_SUBJECTS = {
    '1': ['Hindi', 'English', 'Maths'],
    '2': ['Hindi', 'English', 'Maths'],
    '3': ['Hindi', 'English', 'Maths'],
    '4': ['Hindi', 'English', 'Maths', 'Science', 'EVS'],
    '5': ['Hindi', 'English', 'Maths', 'Science', 'EVS'],
    '6': ['Hindi', 'English', 'Maths', 'Science', 'EVS'],
    '7': ['Hindi', 'Sanskrit', 'Maths', 'English', 'Science', 'SST'],
    '8': ['Hindi', 'Sanskrit', 'Maths', 'English', 'Science', 'SST'],
    '9': ['Hindi', 'Sanskrit', 'Maths', 'English', 'Science', 'SST'],
    '10': ['Hindi', 'Sanskrit', 'Maths', 'English', 'Science', 'SST'],
}

class Student(models.Model):
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    class_name = models.CharField(max_length=10)
    address = models.TextField()
    # ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.name} ({self.roll_number})"

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    marks_obtained = models.FloatField()
    full_marks = models.FloatField(default=50)
    passing_marks = models.FloatField(default=20)
    exam_type = models.CharField(
        max_length=20,
        choices=[
            ('PT-1', 'PT-1'),
            ('PT-2', 'PT-2'),
            ('SA-1', 'SA-1'),
        ],
        default='PT-1'
    )

    def get_grade(self):
        percentage = (self.marks_obtained / self.full_marks) * 100
        if percentage >= 90:
            return "A+"
        elif percentage >= 75:
            return "A"
        elif percentage >= 60:
            return "B"
        elif percentage >= 45:
            return "C"
        elif percentage >= self.passing_marks:
            return "D"
        else:
            return "F"

    def __str__(self):
        return f"{self.student.name} - {self.subject} - {self.exam_type} - {self.marks_obtained}"


class InternalMarks(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, null=True, blank=True)
    exam_type = models.CharField(
        max_length=20,
        choices=[
            ('TERM-1', 'TERM-1')
        ]
    )
    attendance = models.FloatField(default=0)
    notebook = models.FloatField(default=0)
    discipline = models.FloatField(default=0)

    def total_internal(self):
        return self.attendance + self.notebook + self.discipline

    def __str__(self):
        return f"{self.student.name} - {self.exam_type} Internals"
