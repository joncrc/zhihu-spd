import requests
import re
from PIL import Image
import time
import os
import json


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

cookies_filename = "saved_cookies"

sess = requests.Session()


def get_captcha():
    # Return the captcha from manually input

    t = str(int(time.time() * 1000))
    captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + '&type=login'

    response = sess.get(captcha_url, headers=req_header)
    with open('captcha.gif', 'wb') as f:
        f.write(response.content)

    im = Image.open('captcha.gif')
    im.show()
    captcha = input('Please input the captcha value： ')
    os.remove("captcha.gif")
    return captcha


def save_cookies(session, filename=cookies_filename):
    # Save the cookies in the session to file
    with open(filename, 'w') as f:
        f.truncate()
        json.dump(session.cookies.get_dict(), f)


def load_cookies(session, filename=cookies_filename):
    # Load the saved cookies to the session
    with open(filename) as f:
        cookies = json.load(f)
        session.cookies.update(cookies)


def logon(username="", pwd=""):
    # Logon and save cookies in dict format

    if len(username) == 0:
        username = input('Please input the username： ')
    if len(pwd) == 0:
        pwd = input('Please input the password： ')

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
    j = r.json()  # j is dict format
    #print(j)
    c = int(j["r"])
    print(j["msg"])

    if c == 0:
        print("Logon successfully.")
        save_cookies(sess, cookies_filename)
        print("Save cookies successfully.")
    else:
        print("Logon failed.")


def get_logon_sess(username="", pwd=""):
    # Return session with cookies

    try:
        load_cookies(sess, cookies_filename)
        print("Load previous cookie successfully.")
    except Exception as e:
        print("Cookie loading failure. Trying to logon again.")
        print(e)
        logon(username, pwd)

    return sess


def get_logon_cookies(username="", pwd=""):
    # Return cookies in dict format

    cookies_dict = get_logon_sess(username, pwd).cookies.get_dict()
    return cookies_dict


def test_sess_cookies(session):
    # Test logon to verfiy the session has valid cookies
    get_url = 'https://www.zhihu.com/settings/profile'
    resp_code = session.get(get_url, headers=req_header, allow_redirects=False).status_code
    if resp_code == 200:
        return True
    return False


# Test session without cookies
# print(test_sess_cookies(sess))

# Test session with get_logon_sess()
print(test_sess_cookies(get_logon_sess()))

# Test session with get_logon_cookies()
# sess.cookies.update(get_logon_cookies())
# print(test_sess_cookies(sess))
