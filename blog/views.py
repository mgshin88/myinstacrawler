try:
    from django.utils import simplejson as json
except ImportError:
    import json
import cx_Oracle
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.http import require_POST
from .models import Crawler_Filter,Crawler_Tables
from .forms import Generate_Crawling
from .insta import Lets_Crawling,Lets_Work,Lets_Save

def tables(request):
    preList = Crawler_Tables.objects.all()

    return render(request, 'blog/tables.html', {"preList" : preList})

def index(request):
    return render(request, 'blog/index.html',{})

@require_POST
def generate(request):
    #태그 필터
    tagFilter = request.POST.get("tags")
    print(tagFilter)
    #크롤링 횟수
    count = request.POST.get("count")
    print(count)
    #크롤링 시작
    generate = Lets_Crawling(count)
    returnList = generate.crawler()
    #기능수행 후 리턴
    
    #긍정 부정 태그 비율 구하기
    tagList = returnList["tagList"]
    print(tagFilter)
    tagFilter = json.loads(tagFilter)
    print(tagFilter)
    generate = Lets_Work(tagList,tagFilter)
    ratioMap = generate.ratio_Calculator()
    
    print(tagFilter)
    returnList["crawlingList"]["ptag"] = ",".join(tagFilter["ptag"])
    returnList["crawlingList"]["ntag"] = ",".join(tagFilter["ntag"])
    returnList["ratioMap"] = ratioMap
    
    return HttpResponse(json.dumps(returnList), content_type='application/json')

@require_POST
def savedata(request):
    excelList = request.POST.get("excelList")
    excelList = json.loads(excelList)

    crawlingList = request.POST.get("crawlingList")
    crawlingList = json.loads(crawlingList)

    #엑셀 저장
    generate = Lets_Save(excelList)
    result = generate.saveCSV() 
    crawlingList['filename'] = result["filename"]
    
    #db 저장
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",crawlingList)
    # excelupload = pd.read_excel(result["path"]+result["filename"]+".csv", sheet_name="인스타크롤링"+result["filename"],usecols=[0, 1], dtype={0:str, 1:str})
    # rows = [tuple(x) for x in excelupload.to_records(index=False)]
    try:
        # con = cx_Oracle.connect(host="MYTESTCRAWLER.CECYFVIVRUBG.AP-NORTHEAST-2.RDS.AMAZONAWS.COM",
        #                         user='ethan', 
        #                         password='Ehdwns8512',
        #                         db='TESTDB')
        con = cx_Oracle.connect('ethan/Ehdwns8512@MYTESTCRAWLER.CECYFVIVRUBG.AP-NORTHEAST-2.RDS.AMAZONAWS.COM:1521/TESTDB')
        print(con.version)
        cursor = con.cursor()
        selectId = "SELECT MAX(ID)+1 AS ID FROM BLOG_CRAWLER_TABLES"
        cursor.execute(selectId)
        id = cursor.fetchone()
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!idddddd",id)
        inputdata = [str(id[0]),crawlingList["ptag"],crawlingList["ntag"],crawlingList["ttlfeed"],str(crawlingList["crwfeed"]),str(crawlingList["succnt"]),str(crawlingList["failcnt"]),crawlingList["created_at"],crawlingList["updated_at"],crawlingList["working_while"],crawlingList["filename"]] 
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",inputdata)
        statement = "INSERT INTO BLOG_CRAWLER_TABLES (ID,PTAG,NTAG,TTLFEED,CRWFEED,SUCCNT,FAILCNT,CREATED_AT,UPDATED_AT,WORKING_WHILE,FILENAME) VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11)"
        cursor.execute(statement,[2,str(crawlingList["ptag"]),
                                    str(crawlingList["ntag"]),
                                    str(crawlingList["ttlfeed"]),
                                    str(crawlingList["crwfeed"]),
                                    str(crawlingList["succnt"]),
                                    str(crawlingList["failcnt"]),
                                    str(crawlingList["created_at"]),
                                    str(crawlingList["updated_at"]),
                                    str(crawlingList["working_while"]),
                                    str(crawlingList["filename"])])
        con.commit()

        cursor.execute('SELECT COUNT(*) FROM BLOG_CRAWLER_TABLES')
        cnt = cursor.fetchone()
        
        print(cnt)
        result["cnt"] = cnt
    except Exception as e:
        print("errrorrr!!!!!!!!!",e)
        result["cnt"] = 0

    return HttpResponse(json.dumps(result), content_type='application/json')

def sendTag(request):
    initTags = Crawler_Filter.objects.values()[0]

    ntag = initTags["ntag"].split(",")
    ptag = initTags["ptag"].split(",")

    return render(request, 'blog/crawler.html', {'ptag':ptag,'ntag':ntag})
# Create your views here.
