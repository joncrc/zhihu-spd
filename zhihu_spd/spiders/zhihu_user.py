import json

import scrapy
from scrapy import Request

from zhihu_spd.util import logon


class ZhihuUser(scrapy.Spider):
    name = "zhihu_user"

    start_user = "jon-chen"

    # User info URL
    userinfo_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    # User info's include parm
    userinfo_include = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,' \
                       'follower_count,following_count,cover_url,following_topic_count,following_question_count,' \
                       'following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,' \
                       'pins_count,question_count,commercial_question_count,favorite_count,favorited_count,' \
                       'logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,' \
                       'is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,' \
                       'is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,' \
                       'vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,' \
                       'participated_live_count,allow_message,industry_category,org_name,org_homepage,' \
                       'badge[?(type=best_answerer)].topics'

    # He's following
    followees_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?' \
                    'include={include}&offset={offset}&limit={limit}'
    # Fans' list
    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?' \
                    'include={include}&offset={offset}&limit={limit}'
    # Followee and follower's include parm
    follow_include = 'data[*].answer_count, articles_count, gender, follower_count, is_followed, is_following, ' \
                     'badge[?(type = best_answerer)].topics'

    def start_requests(self):

        cookies = logon.get_logon_cookies()
        # Remove the saved_cookies file and provide username and pwd if it needs to use another account
        # cookies = logon.get_logon_cookies(username, pwd)

        get_url = 'https://www.zhihu.com/settings/profile'
        yield Request(url=get_url, cookies=cookies, callback=self.parse_userinfo)

        # Start from the first user
        #yield Request(url=self.userinfo_url.format(user=self.start_user, include=self.userinfo_include),
        #              cookies=cookies, meta={'dont_merge_cookies': True}, callback=self.parse_userinfo)

        # Get the list for whom the user is following
        # yield Request(url=self.followees_url.format(user=self.start_user, include=self.follow_include, offset=0,
        #                                            limit=20), meta={'cookiejar': 1}, callback=self.parse_followees)

    def parse_userinfo(self, response):
        print(response.text)
        data = json.loads(response.text)
        print("--------------------", data)

    def parse_followees(self):
        pass
