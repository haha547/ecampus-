from django.shortcuts import render 
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import re
import sys
from login.models import userData

#################################################################

# Create your views here.
def post(request):
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
            course_URL.append(i["url"])

        user_Dict= dict(zip(course_Name,course_URL))
        soup.decompose = True
        soup.clear()
        #可以存入加密過後的兩個 cookie一個明碼的學號,一個加密的密碼 
        #cCurrAccID之後填入
        try:
            unit = userData.objects.get(cID=cID,cPassword=cPassword)
        except:
            cCurrAccID = find_CurrAccID("http://ecampus.nqu.edu.tw/eCampus3P/Learn/"+ course_URL[0],cID,cPassword)
            print ("there is a user sign in")
            unit = userData.objects.create(cID=cID, cPassword=cPassword, cCurrAccID=cCurrAccID)
            unit.save()    
        return render(request, "course.html", locals())#會跑到course.html模板

def find_CurrAccID (course_url, id_enter, password):#找出CurrAccID這個有點難但是我還是把它弄出來了拉幹
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
        #print (i.get('href')[len(i.get('href'))-46:len(i.get('href'))])
        return i.get('href')[len(i.get('href'))-46:len(i.get('href'))]







"""
def set_cookie(user_name):

cookie = HttpResponse("user")
cookie.set_cookie(user, cID)

def courseLink(request,course_Link):
    return(request,"course.html",locals())






def test (course_url, id_enter, password):#帶入帳號密碼以及課程連結
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
    print(soup.title.string)"""
