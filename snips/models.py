from django.db import models
from .snipqr import create_snipsheet_pdf
import random
import string


class Classroom(models.Model):
    classroom_id = models.CharField(max_length=3, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    semester = models.CharField(max_length=255)
    school = models.CharField(max_length=255)
    email = models.EmailField(max_length=254, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.classroom_id:
            while True:
                new_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))
                if not Classroom.objects.filter(classroom_id=new_id).exists():
                    self.classroom_id = new_id
                    break
        super(Classroom, self).save(*args, **kwargs)

    def __str__(self):
        return self.classroom_id


class Snipsheet(models.Model):
    classroom = models.ForeignKey(Classroom, related_name='snipsheets', on_delete=models.CASCADE)
    snipsheet_id = models.CharField(max_length=255, unique=True, editable=False)

    def create_snips(self):
        existing_snip_ids = set(Snip.objects.filter(snipsheet__classroom=self.classroom)
                                  .values_list('snip_id', flat=True))
        new_snip_ids = set()
        while len(new_snip_ids) < 35:
            random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            new_id = self.classroom.classroom_id + random_string
            if new_id not in existing_snip_ids:
                new_snip_ids.add(new_id)
                existing_snip_ids.add(new_id)
        for code in new_snip_ids:
            Snip.objects.create(snip_id=code, snipsheet=self)

    def save(self, *args, **kwargs):
        if not self.snipsheet_id:
            # Generate snipsheet_id based on classroom_id and number of snipsheets for this classroom
            snipsheet_count = Snipsheet.objects.filter(classroom=self.classroom).count() + 1
            self.snipsheet_id = '{}_{}'.format(self.classroom.classroom_id, snipsheet_count)
        super(Snipsheet, self).save(*args, **kwargs)
        # The creation of snips is moved here to ensure snipsheet_id is set before creating snips
        self.create_snips()
        # Finally, create a pdf file with qr-codes for the snips
        create_snipsheet_pdf(self.snips.all().values_list('snip_id', flat=True), self.snipsheet_id)

    def __str__(self):
        return self.snipsheet_id


class Snip(models.Model):
    snipsheet = models.ForeignKey(Snipsheet, related_name='snips', on_delete=models.CASCADE)
    snip_id = models.CharField(max_length=9)
    student_id = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.snip_id
