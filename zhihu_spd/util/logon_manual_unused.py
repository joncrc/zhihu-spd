import requests
import re
from PIL import Image
import time
import os
import http.cookiejar

req_header = {'Accept': '*/*',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
              'Connection': 'keep-alive',
              'Host': 'www.zhihu.com',
              'Origin': 'https://www.zhihu.com',
              'Referer': 'https://www.zhihu.com/',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/57.0.2987.133 Safari/537.36',
              }

zhihu_url = 'https://www.zhihu.com'
login_type_url = ''

sess = requests.Session()


def get_captcha():
    # Return the captcha value

    t = str(int(time.time() * 1000))
    captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + '&type=login'

    response = sess.get(captcha_url, headers=req_header)
    with open('captcha.gif', 'wb') as f:
        f.write(response.content)
    # Pillow显示验证码
    im = Image.open('captcha.gif')
    im.show()
    captcha = input('Please input the captcha value： ')
    os.remove("captcha.gif")
    return captcha


def logon(username, pwd):
    # Logon method, return cookies

    # Get the xsrf value
    r = sess.get(zhihu_url, headers=req_header, verify=True)
    # print(r.text)
    xsrf = re.findall('name="_xsrf" value="([\S\s]*?)"', r.text)[0]
    # print(xsrf)

    # Prepare Form Data
    form_data = {'_xsrf': xsrf, 'password': pwd, 'remember_me': 'true'}

    if re.match(r'\d{11}$', username):
        print("Logon using mobile phone number.")
        form_data['phone_num'] = username
        login_type_url = '/login/phone_num'

    elif re.search(r'(.+)@(.+)', username):
        print("Logon using email address.")
        form_data['email'] = username
        login_type_url = '/login/email'

    else:
        print("Incorrect username format. Must be phone number or email address.")
        exit(1)

    form_data["captcha"] = get_captcha()

    # print(form_data)

    r = sess.post(zhihu_url + login_type_url, data=form_data, headers=req_header, verify=True)
    j = r.json()  # j is a dict format
    #print(j)
    c = int(j["r"])
    print(j["msg"])

    if c == 0:
        print("Logon successfully.")
        sess.cookies.save(ignore_discard=True, ignore_expires=True)
        print("Save cookies successfully.")
    else:
        print("Logon failed.")


def get_logon_sess(username="", pwd=""):
    # Return session with cookie

    # Load cookie
    cookie_filename = 'saved_cookies'
    sess.cookies = http.cookiejar.LWPCookieJar(cookie_filename)
    # LWPCookieJar is a sub class of FileCookieJar. Save the cookie as Set-Cookie3 format.
    # Another option is to use MozillaCookieJar. Save as .txt format.

    try:
        sess.cookies.load(filename=cookie_filename, ignore_discard=True)
        print("Load previous cookie successfully.")
    except Exception as e:
        print("Cookie loading failure. Trying to logon again.")
        print(e)
        logon(username, pwd)

    # Test the logon
    # get_url = 'https://www.zhihu.com/settings/profile'
    # resp = sess.get(get_url, headers=req_header, allow_redirects=False)
    #
    # print(resp.text)

    return sess


def get_logon_cookie(username="", pwd=""):
    # Return cookie

    cookies = get_logon_sess(username, pwd).cookies

    return cookies
