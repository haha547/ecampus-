from django.shortcuts import render 
from django.http import HttpResponse
from bs4 import BeautifulSoup#尋找html檔
from login.models import userData
from datetime import datetime
import requests, re, sys, os, pyrebase, firebase_admin, gc
config = {
    "apiKey": "AIzaSyBzIE28WS3omyQgfeoz_3h2qcyu_KzD_Wg",
    "authDomain": "nquyes.firebaseapp.com",
    "databaseURL": "https://nquyes.firebaseio.com",
    "projectId": "nquyes",
    "storageBucket": "nquyes.appspot.com",
    "messagingSenderId": "659605466677"
  }
firebase= pyrebase.initialize_app(config)

#################################################################

# Create your views here.
def post(request):
    ##########################################################
    #############新使用者先建立DIR再用這個DIR要爬的東西#############
    ##############因為我們要一個介面解決這他媽改死的教學平台##########
    ###########################################################
    if request.method == "POST":#以下是爬蟲程式
        cID = request.POST ['stuID']
        cPassword = request.POST ['pwd']
        url = "http://ecampus.nqu.edu.tw/eCampus3P/Learn/LoginPage2/product_login.aspx"#ecampus的login url
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
        #headers還不知道怎麼抓但是我想都差不多一樣
        resp = requests.post(url, headers = headers , data={
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '', 
            '__VIEWSTATE': ' /wEPDwUKMjAzODk5NzA3Mg8WAh4EX2N0bAUMYnRuTG9naW5IZWxwFgICAw9kFiYCAQ8WAh4KYmFja2dyb3VuZAUWaW1hZ2VzL3poLVRXL2xvZ2luLmdpZhYMAgEPFgIeBXN0eWxlBRpwb3NpdGlvbjpyZWxhdGl2ZTtsZWZ0OjBweBYCAgEPDxYCHghJbWFnZVVybAUTaW1hZ2VzL3poLVRXL2lkLmdpZmRkAgMPFgIfAgUacG9zaXRpb246cmVsYXRpdmU7bGVmdDowcHhkAgUPFgIfAgUacG9zaXRpb246cmVsYXRpdmU7bGVmdDowcHgWAmYPZBYCAgEPDxYCHwMFGWltYWdlcy96aC1UVy9wYXNzd29yZC5naWZkZAIHDxYCHwIFGnBvc2l0aW9uOnJlbGF0aXZlO2xlZnQ6MHB4ZAIJD2QWCAIBDw8WBh4IQ3NzQ2xhc3MFC21lbnVfdGV4dDAyHgRUZXh0BQ5b5b+Y6KiY5a+G56K8XR4EXyFTQgICZGQCAw8PFgYfBAUQbWVudV90ZXh0MDJfb190dx8FBQ5b55m75YWl6Kqq5piOXR8GAgJkZAIFDw8WBh8EBQttZW51X3RleHQwMh8FBQ5b6Kiq5a6i5Y+D6KeAXR8GAgJkZAIHDw8WCB8EBQttZW51X3RleHQwMh8FBQ5b5Y+D6KeA6Kqy56iLXR8GAgIeB1Zpc2libGVoZGQCCw8PFgIfAwUcaW1hZ2VzL3poLVRXL2xvZ2luIEVudGVyLmpwZxYEHgtvbm1vdXNlb3ZlcgU4amF2YXNjcmlwdDp0aGlzLnNyYz0naW1hZ2VzL3poLVRXL2xvZ2luIEVudGVyX292ZHcuanBnJzseCm9ubW91c2VvdXQFM2phdmFzY3JpcHQ6dGhpcy5zcmM9J2ltYWdlcy96aC1UVy9sb2dpbiBFbnRlci5qcGcnO2QCAw8PFgIfAwUTaW1hZ2VzL3poLVRXL0dCLmdpZmRkAgQPDxYCHwMFE2ltYWdlcy96aC1UVy9Fbi5naWZkZAIGDw8WAh8DBRZpbWFnZXMvemgtVFcvdGl0ZWwuanBnZGQCCA8PFgYfBAULbWVudV90ZXh0MDIfBQUOW+ebuOmXnOmAo+e1kF0fBgICZGQCCg8PFgYfBAULbWVudV90ZXh0MDIfBQUOW+W5s+WPsOS7i+e0uV0fBgICZGQCDA8PFgYfBAULbWVudV90ZXh0MDIfBQUOW+W4uOimi+WVj+mhjF0fBgICZGQCDg8PFgYfBAULbWVudV90ZXh0MDIfBQUOW+mAo+e1oeaIkeWAkV0fBgICZGQCEA8PFggfBAULbWVudV90ZXh0MDIfBQUOW+eUs+iri+W4s+iZn10fBgICHwdoZGQCFA8PFgIfAwUdaW1hZ2VzL3poLVRXL21haW4gcGljdHVyZS5qcGdkZAIWDxYCHwEFH2ltYWdlcy96aC1UVy9sb2dpbiB0ZXh0IHBhbi5qcGdkAhgPDxYCHwMFFWltYWdlcy96aC1UVy9uZXdzLmpwZ2RkAhwPDxYCHwMFGmltYWdlcy96aC1UVy9mcmFtZV90b3AuZ2lmZGQCHg8WAh8BBR9pbWFnZXMvemgtVFcvbG9naW4gdGV4dCBwYW4uanBnZAIgDxYEHgZoZWlnaHQFBTI0MHB4HgNzcmMFFy4uL2xvZ2luX0hlbHBJbmRleC5hc3B4ZAIiDxYCHwEFGGltYWdlcy96aC1UVy9mcmFtZV9SLmdpZmQCJA8PFgIfAwUaaW1hZ2VzL3poLVRXL2ZyYW1lX2Rvdy5naWZkZAIoDxYEHwUFHGVDYW1wdXMgSUlJIHYxLjYuMDkxOTguMDEwNDAfB2dkAi4PDxYCHwMFH2ltYWdlcy96aC1UVy9sb2dvIG9mIDNwcm9iZS5naWZkZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAwUIYnRuTG9naW4FCmJ0bkNoaW5lc2UFCmJ0bkVuZ2xpc2hqzHG9hdaHqyty7OyKa8boh3mpUA==',
            '__VIEWSTATEGENERATOR': '8B4B7C2A',
            'txtLoginId': cID,# studentID
            'txtLoginPwd': cPassword,# password
            'btnLogin.x' : '44',#應該填多少也沒差
            'btnLogin.y' : '25',#應該填多少也沒差
        })
        soup = BeautifulSoup(resp.text,"lxml")
        course_Name=[]
        course_URL=[]
        for i in soup.find_all(id = re.compile("CourseName")):
            course_Name.append(i.string)
        for i in soup.find_all("input",{'url': re.compile('stu_course_default.aspx?')}):
            course_URL.append(i["url"][33:69])
        cName= soup.find(id="ctl00_lbAccount").string
        user_Dict= dict(zip(course_Name,course_URL)) 
        if len(user_Dict) == 0:
            return render(request, "error_login.html",eooro_login = True)#回傳到index做登入錯誤
        soup.decompose = True
        soup.clear()
        try:
            unit = userData.objects.get(cID=cID, cPassword=cPassword)
            print("有人登入拉")
        except:
            cCurrAccID = find_CurrAccID("http://ecampus.nqu.edu.tw/eCampus3P/Learn/stu_course_default.aspx?CourseId="+ course_URL[0]+"&Role=Student",cID,cPassword)
            unit = userData.objects.create(cID=cID, cPassword=cPassword, cCurrAccID=cCurrAccID[10:], cName=cName)
            unit.save()
            print("有人創帳號嘍")
        request.session ["user_id"] = cID #設定本站的session
        return render(request, "course/course.html", locals())#會跑到course.html模板


def find_CurrAccID (course_url, id_enter, password):#找出CurrAccID
    s= requests.session()
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    login_DataFrom = {'__EVENTTARGET': '',
        '__EVENTARGUMENT': '', 
        '__VIEWSTATE': ' /wEPDwUKMjAzODk5NzA3Mg8WAh4EX2N0bAUMYnRuTG9naW5IZWxwFgICAw9kFiYCAQ8WAh4KYmFja2dyb3VuZAUWaW1hZ2VzL3poLVRXL2xvZ2luLmdpZhYMAgEPFgIeBXN0eWxlBRpwb3NpdGlvbjpyZWxhdGl2ZTtsZWZ0OjBweBYCAgEPDxYCHghJbWFnZVVybAUTaW1hZ2VzL3poLVRXL2lkLmdpZmRkAgMPFgIfAgUacG9zaXRpb246cmVsYXRpdmU7bGVmdDowcHhkAgUPFgIfAgUacG9zaXRpb246cmVsYXRpdmU7bGVmdDowcHgWAmYPZBYCAgEPDxYCHwMFGWltYWdlcy96aC1UVy9wYXNzd29yZC5naWZkZAIHDxYCHwIFGnBvc2l0aW9uOnJlbGF0aXZlO2xlZnQ6MHB4ZAIJD2QWCAIBDw8WBh4IQ3NzQ2xhc3MFC21lbnVfdGV4dDAyHgRUZXh0BQ5b5b+Y6KiY5a+G56K8XR4EXyFTQgICZGQCAw8PFgYfBAUQbWVudV90ZXh0MDJfb190dx8FBQ5b55m75YWl6Kqq5piOXR8GAgJkZAIFDw8WBh8EBQttZW51X3RleHQwMh8FBQ5b6Kiq5a6i5Y+D6KeAXR8GAgJkZAIHDw8WCB8EBQttZW51X3RleHQwMh8FBQ5b5Y+D6KeA6Kqy56iLXR8GAgIeB1Zpc2libGVoZGQCCw8PFgIfAwUcaW1hZ2VzL3poLVRXL2xvZ2luIEVudGVyLmpwZxYEHgtvbm1vdXNlb3ZlcgU4amF2YXNjcmlwdDp0aGlzLnNyYz0naW1hZ2VzL3poLVRXL2xvZ2luIEVudGVyX292ZHcuanBnJzseCm9ubW91c2VvdXQFM2phdmFzY3JpcHQ6dGhpcy5zcmM9J2ltYWdlcy96aC1UVy9sb2dpbiBFbnRlci5qcGcnO2QCAw8PFgIfAwUTaW1hZ2VzL3poLVRXL0dCLmdpZmRkAgQPDxYCHwMFE2ltYWdlcy96aC1UVy9Fbi5naWZkZAIGDw8WAh8DBRZpbWFnZXMvemgtVFcvdGl0ZWwuanBnZGQCCA8PFgYfBAULbWVudV90ZXh0MDIfBQUOW+ebuOmXnOmAo+e1kF0fBgICZGQCCg8PFgYfBAULbWVudV90ZXh0MDIfBQUOW+W5s+WPsOS7i+e0uV0fBgICZGQCDA8PFgYfBAULbWVudV90ZXh0MDIfBQUOW+W4uOimi+WVj+mhjF0fBgICZGQCDg8PFgYfBAULbWVudV90ZXh0MDIfBQUOW+mAo+e1oeaIkeWAkV0fBgICZGQCEA8PFggfBAULbWVudV90ZXh0MDIfBQUOW+eUs+iri+W4s+iZn10fBgICHwdoZGQCFA8PFgIfAwUdaW1hZ2VzL3poLVRXL21haW4gcGljdHVyZS5qcGdkZAIWDxYCHwEFH2ltYWdlcy96aC1UVy9sb2dpbiB0ZXh0IHBhbi5qcGdkAhgPDxYCHwMFFWltYWdlcy96aC1UVy9uZXdzLmpwZ2RkAhwPDxYCHwMFGmltYWdlcy96aC1UVy9mcmFtZV90b3AuZ2lmZGQCHg8WAh8BBR9pbWFnZXMvemgtVFcvbG9naW4gdGV4dCBwYW4uanBnZAIgDxYEHgZoZWlnaHQFBTI0MHB4HgNzcmMFFy4uL2xvZ2luX0hlbHBJbmRleC5hc3B4ZAIiDxYCHwEFGGltYWdlcy96aC1UVy9mcmFtZV9SLmdpZmQCJA8PFgIfAwUaaW1hZ2VzL3poLVRXL2ZyYW1lX2Rvdy5naWZkZAIoDxYEHwUFHGVDYW1wdXMgSUlJIHYxLjYuMDkxOTguMDEwNDAfB2dkAi4PDxYCHwMFH2ltYWdlcy96aC1UVy9sb2dvIG9mIDNwcm9iZS5naWZkZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAwUIYnRuTG9naW4FCmJ0bkNoaW5lc2UFCmJ0bkVuZ2xpc2hqzHG9hdaHqyty7OyKa8boh3mpUA==',
        '__VIEWSTATEGENERATOR': '8B4B7C2A',
        'txtLoginId': id_enter,
        'txtLoginPwd': password,
        'btnLogin.x' : '42',
        'btnLogin.y' : '25',}
    q= s.get(course_url, headers=headers)#用課程連結進去拿到session
    p= s.post(q.url, headers=headers, data=login_DataFrom)#登入取得coolies跟session
    r= s.get("http://ecampus.nqu.edu.tw/eCampus3P/Learn/stu_announcement_online.aspx", headers=headers)
    soup = BeautifulSoup(r.text,"lxml")
    for i in soup.find_all("a", {'href': re.compile('CurrAccId')},limit=1):
        return i.get('href')[len(i.get('href'))-46:len(i.get('href'))]


def get_Course_EveryThing(request, enterNum):#給課程id, 進入課程, 爬公告
    unit = userData.objects.get(cID = request.session ["user_id"])#從session 抓你的帳號 比對資料庫然後抓帳號密碼
    s= requests.session()
    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
    login_DataFrom = {'__EVENTTARGET': '',
        '__EVENTARGUMENT': '', 
        '__VIEWSTATE': ' /wEPDwUKMjAzODk5NzA3Mg8WAh4EX2N0bAUMYnRuTG9naW5IZWxwFgICAw9kFiYCAQ8WAh4KYmFja2dyb3VuZAUWaW1hZ2VzL3poLVRXL2xvZ2luLmdpZhYMAgEPFgIeBXN0eWxlBRpwb3NpdGlvbjpyZWxhdGl2ZTtsZWZ0OjBweBYCAgEPDxYCHghJbWFnZVVybAUTaW1hZ2VzL3poLVRXL2lkLmdpZmRkAgMPFgIfAgUacG9zaXRpb246cmVsYXRpdmU7bGVmdDowcHhkAgUPFgIfAgUacG9zaXRpb246cmVsYXRpdmU7bGVmdDowcHgWAmYPZBYCAgEPDxYCHwMFGWltYWdlcy96aC1UVy9wYXNzd29yZC5naWZkZAIHDxYCHwIFGnBvc2l0aW9uOnJlbGF0aXZlO2xlZnQ6MHB4ZAIJD2QWCAIBDw8WBh4IQ3NzQ2xhc3MFC21lbnVfdGV4dDAyHgRUZXh0BQ5b5b+Y6KiY5a+G56K8XR4EXyFTQgICZGQCAw8PFgYfBAUQbWVudV90ZXh0MDJfb190dx8FBQ5b55m75YWl6Kqq5piOXR8GAgJkZAIFDw8WBh8EBQttZW51X3RleHQwMh8FBQ5b6Kiq5a6i5Y+D6KeAXR8GAgJkZAIHDw8WCB8EBQttZW51X3RleHQwMh8FBQ5b5Y+D6KeA6Kqy56iLXR8GAgIeB1Zpc2libGVoZGQCCw8PFgIfAwUcaW1hZ2VzL3poLVRXL2xvZ2luIEVudGVyLmpwZxYEHgtvbm1vdXNlb3ZlcgU4amF2YXNjcmlwdDp0aGlzLnNyYz0naW1hZ2VzL3poLVRXL2xvZ2luIEVudGVyX292ZHcuanBnJzseCm9ubW91c2VvdXQFM2phdmFzY3JpcHQ6dGhpcy5zcmM9J2ltYWdlcy96aC1UVy9sb2dpbiBFbnRlci5qcGcnO2QCAw8PFgIfAwUTaW1hZ2VzL3poLVRXL0dCLmdpZmRkAgQPDxYCHwMFE2ltYWdlcy96aC1UVy9Fbi5naWZkZAIGDw8WAh8DBRZpbWFnZXMvemgtVFcvdGl0ZWwuanBnZGQCCA8PFgYfBAULbWVudV90ZXh0MDIfBQUOW+ebuOmXnOmAo+e1kF0fBgICZGQCCg8PFgYfBAULbWVudV90ZXh0MDIfBQUOW+W5s+WPsOS7i+e0uV0fBgICZGQCDA8PFgYfBAULbWVudV90ZXh0MDIfBQUOW+W4uOimi+WVj+mhjF0fBgICZGQCDg8PFgYfBAULbWVudV90ZXh0MDIfBQUOW+mAo+e1oeaIkeWAkV0fBgICZGQCEA8PFggfBAULbWVudV90ZXh0MDIfBQUOW+eUs+iri+W4s+iZn10fBgICHwdoZGQCFA8PFgIfAwUdaW1hZ2VzL3poLVRXL21haW4gcGljdHVyZS5qcGdkZAIWDxYCHwEFH2ltYWdlcy96aC1UVy9sb2dpbiB0ZXh0IHBhbi5qcGdkAhgPDxYCHwMFFWltYWdlcy96aC1UVy9uZXdzLmpwZ2RkAhwPDxYCHwMFGmltYWdlcy96aC1UVy9mcmFtZV90b3AuZ2lmZGQCHg8WAh8BBR9pbWFnZXMvemgtVFcvbG9naW4gdGV4dCBwYW4uanBnZAIgDxYEHgZoZWlnaHQFBTI0MHB4HgNzcmMFFy4uL2xvZ2luX0hlbHBJbmRleC5hc3B4ZAIiDxYCHwEFGGltYWdlcy96aC1UVy9mcmFtZV9SLmdpZmQCJA8PFgIfAwUaaW1hZ2VzL3poLVRXL2ZyYW1lX2Rvdy5naWZkZAIoDxYEHwUFHGVDYW1wdXMgSUlJIHYxLjYuMDkxOTguMDEwNDAfB2dkAi4PDxYCHwMFH2ltYWdlcy96aC1UVy9sb2dvIG9mIDNwcm9iZS5naWZkZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAwUIYnRuTG9naW4FCmJ0bkNoaW5lc2UFCmJ0bkVuZ2xpc2hqzHG9hdaHqyty7OyKa8boh3mpUA==',
        '__VIEWSTATEGENERATOR': '8B4B7C2A',
        'txtLoginId': unit.cID,
        'txtLoginPwd': unit.cPassword,
        'btnLogin.x' : '42',
        'btnLogin.y' : '25',}
    q= s.get("http://ecampus.nqu.edu.tw/eCampus3P/Learn/stu_course_default.aspx?CourseId="+enterNum+"&Role=Student", headers=headers)#用課程連結進去拿到session
    p= s.post(q.url, headers=headers, data=login_DataFrom)#登入取得coolies跟session
    stu_announcement= s.get("http://ecampus.nqu.edu.tw/eCampus3P/Learn/stu_announcement_online.aspx")
    soup = BeautifulSoup(stu_announcement.text, "lxml")
    announcement_title =[]#公告標題
    announcement_time =[]#公告日期
    announcement_text =[]#公告內容
    announcement_total =[]#合起來放在html上一個for迴圈出來
    for i in soup.find_all("span", id=re.compile("_lbCaption")):#公告標題
        announcement_title.append(i.string.strip())
    for i in soup.find_all("span", id=re.compile("_lbBeginDate")):#公告日期
        announcement_time.append(i.string.strip())
    for i in soup.find_all("span", id=re.compile("_lbContent")):#公告內容
        announcement_text.append(i.get_text().strip())#因為有些會有在span中會有一些很奇怪的東西不能用string
    announcement_total= zip(announcement_title,announcement_time,announcement_text)#這要丟到html裡面 順序為 標題 日期 公告
    soup.decompose = True
    soup.clear()

    course_DOC_Name =[]
    course_DOC_URL =[]
    course_DOC_Total=[]
    doc=s.get("http://ecampus.nqu.edu.tw/eCampus3P/Learn/stu_materials_default.aspx?CurrCourseId="+enterNum+"&CurrRole=Student&CurrAccId="+unit.cCurrAccID)#我
    soup = BeautifulSoup(doc.text,"lxml") 
    for i in soup.find_all("tr", class_= re.compile("Tbl")):
        course_DOC_Name.append(i.find("td").get_text())
    for i in soup.find_all("input", onclick= re.compile("openDialog_hWin")):
        course_DOC_URL.append(i["onclick"][79:115])
    for i in soup.find_all("tr", style="overflow:hidden;"):#找公告時間
        for u in i.find_all(style="overflow:hidden;")[5]:
            if len(u.string) == 22:
                a= datetime.strptime(u.string[0:10], "%Y/%m/%d")
                print(a)
            elif len(u.string) == 21 :
                a= datetime.strptime(u.string[0:9], "%Y/%m/%d")
                print(a)
            else :
                a= datetime.strptime(u.string[0:8], "%Y/%m/%d")
                print(a) 
    course_DOC_Total= dict(zip(course_DOC_Name, course_DOC_URL))
    
    soup.decompose = True
    soup.clear()
    hw= s.get("http://ecampus.nqu.edu.tw/eCampus3P/Learn/stu_materials_homework_list.aspx?CurrCourseId="+enterNum+"&CurrRole=Student&CurrAccId="+unit.cCurrAccID)
    soup= BeautifulSoup(hw.text, "lxml")#抓到功課頁面我好帥我好厲害ㄏ
    hw_list_Name=[]
    hw_list_DeadTime=[]
    return render(request, "course/courseInfo.html", locals())#會跑到course.html模板
    ##以下要清空查到的東西
    del course_DOC_Total, course_DOC_Name, course_DOC_URL, hw_list_DeadTime, hw_list_Name, announcement_info, announcement_text, announcement_time, announcement_time, announcement_title
    gc.collect()