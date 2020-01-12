from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

# 동적페이지 크롤링을 위하여 selenium 라이브러리를 사용

class Crawler:
    def __init__(self):
        # delay시간 지정
        self.delay = 3
        # chromedriver 위치
        self.path = "C:/chromedriver.exe"
        self.nick, self.contents, self.recomm, self.unrecomm = [], [], [], []
        self.title, self.play, self.like, self.episode, self.reple_count = [], [], [], [], []
        self.age_10, self.age_20, self.age_30, self.age_40, self.age_50, self.age_60 = [], [], [], [], [], []
        # 초기 page number
        self.page_num = 2
        # page 갯수
        self.cnt_page = 0

    # 리플들을 가져온다.
    def get_reple(self, start_url):

        # 가져온 url이 담기 배열을 for문으로 돌려준다.
        for url in start_url:
            # Chrome webdriver를 이용하여 브라우저에 접근한다.
            browser = webdriver.Chrome(self.path)
            browser.implicitly_wait(self.delay)
            browser.get(url)

            # 태그중 body를 가져온다.
            body = browser.find_element_by_tag_name('body')

            # 페이지를 3번 스크롤다운 해 준다.
            num_of_pagedowns = 3
            while num_of_pagedowns:
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(2)
                num_of_pagedowns -= 1

            self.make_htmls(browser, url)

    # 실제 html에 접근한다.
    def make_htmls(self, browser, url):
        # BeautifulSoup을 이용해 html태그들을 가져온다.
        html = BeautifulSoup(browser.page_source, 'html.parser')

        # page number를 초기화 해 준다.
        self.set_init_page(html)

        # page number를 계산해준다.
        for i in range(1, self.page_num):
            time.sleep(2)
            html = BeautifulSoup(browser.page_source, 'html.parser')
            self.get_vals(html)
            if self.cnt_page is not None and i + 1 == self.page_num:
                browser.find_elements_by_xpath('//*[@class="u_cbox_next"][1]')[0].click()
                self.make_htmls(browser, url)
            elif i + 1 == self.page_num:
                return
            elif self.cnt_page is not None:
                browser.find_elements_by_xpath('//*[@class="u_cbox_page"][' + str(i) + ']')[0].click()

    def get_vals(self, html):
        # page number를 초기화 해 준다.
        self.set_init_page(html)

        # 각각의 정보들을 html 태그를 통해 가져온다.
        title = html.find('h3', {'class': '_clipTitle'})
        play = html.find('span', {'class': 'play'})
        like = html.find('em', {'class': 'u_cnt _cnt'})
        episode = html.find('dl', {'class': 'rating_list'}).find_all('dd', {'class': 'col'})[2]
        reple_count = html.find('span', {'class': 'count _commentCount'})
        age_10 = html.find_all('div', {'class': 'u_cbox_chart_progress'})[0].find('span', {'class': 'u_cbox_chart_per'})
        age_20 = html.find_all('div', {'class': 'u_cbox_chart_progress'})[1].find('span', {'class': 'u_cbox_chart_per'})
        age_30 = html.find_all('div', {'class': 'u_cbox_chart_progress'})[2].find('span', {'class': 'u_cbox_chart_per'})
        age_40 = html.find_all('div', {'class': 'u_cbox_chart_progress'})[3].find('span', {'class': 'u_cbox_chart_per'})
        age_50 = html.find_all('div', {'class': 'u_cbox_chart_progress'})[4].find('span', {'class': 'u_cbox_chart_per'})
        age_60 = html.find_all('div', {'class': 'u_cbox_chart_progress'})[5].find('span', {'class': 'u_cbox_chart_per'})

        for li in html.find_all('div', {'class': 'u_cbox_area'}):
            nick = li.find('span', {'class': 'u_cbox_nick'})
            contents = li.find('span', {'class': 'u_cbox_contents'})
            recomm = li.find('em', {'class': 'u_cbox_cnt_recomm'})
            unrecomm = li.find('em', {'class': 'u_cbox_cnt_unrecomm'})

            # html 태그로부터 가져온 정보들을 전역변수에 넣어준다.
            if nick and contents and recomm and unrecomm is not None:
                self.nick.append(nick.get_text(" ", strip=True))
                self.contents.append(contents.get_text(" ", strip=True))
                self.recomm.append(recomm.get_text(" ", strip=True))
                self.unrecomm.append(unrecomm.get_text(" ", strip=True))
                self.title.append(title.get_text(" ", strip=True))
                self.play.append(play.get_text(" ", strip=True))
                self.like.append(like.get_text(" ", strip=True))
                self.reple_count.append(reple_count.get_text(" ", strip=True))
                self.episode.append(episode.get_text(" ", strip=True))
                self.age_10.append(age_10.get_text(" ", strip=True))
                self.age_20.append(age_20.get_text(" ", strip=True))
                self.age_30.append(age_30.get_text(" ", strip=True))
                self.age_40.append(age_40.get_text(" ", strip=True))
                self.age_50.append(age_50.get_text(" ", strip=True))
                self.age_60.append(age_60.get_text(" ", strip=True))

    # page number 초기화 함수.
    def set_init_page(self, html):
        self.cnt_page = html.find('a', {'class': 'u_cbox_next'})
        cnt_num = 1
        if self.cnt_page is not None:
            cnt_num = 2
        self.page_num = len(html.find_all('span', {'class': 'u_cbox_num_page'})) + cnt_num

# 각 url들을 배열로 받아 파라미터로 전달한다.
urls = ['https://tv.naver.com/v/5463510', 'https://tv.naver.com/v/5464028',
        'https://tv.naver.com/v/5464095', 'https://tv.naver.com/v/5463616']

# 크롤러 객체를 생성
crawler = Crawler()

# 리플 정보들을 가져온다.
crawler.get_reple(urls)

# 가져온 정보들을 dataframe 형태로 만들어준다.
df = pd.DataFrame([crawler.nick, crawler.contents, crawler.recomm, crawler.unrecomm,
                   crawler.title, crawler.play, crawler.like, crawler.reple_count, crawler.episode,
                   crawler.age_10, crawler.age_20, crawler.age_30, crawler.age_40, crawler.age_50, crawler.age_60]).T
# Column들의 이름을 지정해준다.
df.columns = ['nick', 'contents', 'recomm', 'unrecomm', 'title', 'play', 'like', 'reple_count', 'episode',
              'age_10', 'age_20', 'age_30', 'age_40', 'age_50', 'age_60']
print(df)

# csv파일로 저장해준다.
df.to_csv('file2.csv', encoding='utf-8-sig')