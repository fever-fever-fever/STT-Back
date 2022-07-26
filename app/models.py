from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
# Create your models here.
class Video(models.Model):
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    date = models.DateField()

    class Meta:
        db_table = 'video_table'
    
    def publish(self):
        self.save()

class Video_word(models.Model):
    
    wid = models.AutoField(primary_key=True)
    video_id = models.ForeignKey('Video', on_delete=CASCADE, db_column='video_id')
    word = models.CharField(max_length=200)
    start_time = models.FloatField()
    end_time = models.FloatField()
    date = models.DateField()
    
    class Meta:
        db_table = 'video_word_table'
    
    def publish(self):
        self.save()
