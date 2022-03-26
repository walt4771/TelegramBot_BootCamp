import requests
import getData


class TheCamp:
    def __init__(self, userId, userPwd, title, content):
        self.session = requests.Session()

        self.userId = userId
        self.userPwd = userPwd

        self.content = content
        self.title = title

        self.session.headers['User-Agent'] \
            = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 ' \
              'Safari/537.36 '

    def login(self):
        url = 'https://www.thecamp.or.kr/login/loginA.do'

        data = {
            'userId': self.userId,
            'userPwd': self.userPwd,
        }

        resp = self.session.post(url, data=data)
        print(resp.text + str(resp.status_code))

    def sendMessage(self):
        url = 'https://www.thecamp.or.kr/consolLetter/insertConsolLetterA.do?'

        data = {
            'traineeMgrSeq': 'xxxxxxx',
            'sympathyLetterSubject': self.title,
            'sympathyLetterContent': self.content,
            'boardDiv': 'sympathyLetter',
            'tempSaveYn': 'N',
        }

        resp = self.session.post(url, data=data)
        print(resp.text + str(resp.status_code))


weather = getData.getWeather()
tMessage = getData.getTelegramMessage()
news = '# 과학기술' + getData.getSciNews_tech() + '<br><br># 과학정책<br>' + getData.getSciNews_policy() + '<br><br># 과학문화<br>' + getData.getSciNews_culture()

camp = TheCamp('userId', 'userPw', '기견아 인편왔다!! ' + getData.today, tMessage + '<br><br>' + str(weather) + '<br><br>' + news)
camp.login()
camp.sendMessage()

tongilnews = getData.getNews_tongil()

camp = TheCamp('userId', 'userPw', '다른 소식들 ' + getData.today, tongilnews)
camp.login()
camp.sendMessage()
