from django.db import models
from django.utils import timezone


class Crawler_Tables(models.Model):
        #긍정태그 필터
        ptag = models.CharField(max_length=1000)
        #부정태그 필터
        ntag = models.CharField(max_length=1000)
        #이전에 실행된 크롤링 데이터
        ttlfeed = models.CharField(max_length=30)
        crwfeed = models.CharField(max_length=30)
        succnt = models.CharField(max_length=10)
        failcnt = models.CharField(max_length=10)
        created_at = models.CharField(max_length=20)
        updated_at = models.CharField(max_length=20)
        working_while = models.CharField(max_length=20)
        filename = models.CharField(max_length=20)
        

class Crawler_Filter(models.Model):
        ptag = models.CharField(max_length=1000)
        ntag = models.CharField(max_length=1000)

# Create your models here.
