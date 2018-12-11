from selenium import webdriver
from time import sleep
import csv

def get_page_num():
    review_num=d.find_element_by_xpath('//*[@class="score_total"]/strong/em').text
    review_num=review_num.replace(",","")
    page_num=((int(review_num)-1)//10) + 1
    page_num= page_num if page_num>=1 else 1

    return page_num

def get_reviews(page_num, released, genre):
    result=list()
    for j in range(1, page_num+1):
        sleep(2)
        page_xpath='//*[@id="pagerTagAnchor'+str(j)+'"]'
        d.find_element_by_xpath(page_xpath).click()

        for i in range(1,11):
            try:
                root_xpath='//*[@class="score_result"]/ul/li['+str(i)+']'
                score_xpath=root_xpath+'/div[@class="star_score"]/em'
                review_xpath=root_xpath+'/div[@class="score_reple"]/p'
                time_xpath=root_xpath+'/div[@class="score_reple"]/dl/dt/em[2]'
                score=d.find_element_by_xpath(score_xpath).text
                review=d.find_element_by_xpath(review_xpath).text
                re_time=d.find_element_by_xpath(time_xpath).text
                print("score: {}, review: {}, time:{}".format(score, review, re_time))
                result.append({'score':score, 'review':review, 'time':re_time, 'released':released, 'genre':genre})
            except:
                print("no xpath found")
                pass

        if j%10==0 or j==page_num:
            with open('./review_{}_{}.csv'.format(genre, movie_title), 'a', encoding='utf8') as csvfile:
                fieldnames=["score", "review", "time", "released", "genre"]
                writer=csv.DictWriter(csvfile, fieldnames=fieldnames)

                for l in range(len(result)):
                    writer.writerow(result[l])
            result=list()


#WINDOWS OS
header = {'User-Agent': ''}

options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36")
# options.add_argument('--incognito')

d = webdriver.Chrome(executable_path='./chromedriver', chrome_options=options)
# d=webdriver.Chrome(executable_path='./chromedriver', chrome_options=options) #MAC OS인 경우 이걸로 하세요, 윗줄 주석 처리
# d = webdriver.Chrome(executable_path='./chromedriver.exe')
d.implicitly_wait(3)

with open('./movie_genre_korea.csv', 'r') as csvfile:
    list_reader=csv.reader(csvfile, delimiter=',')
    movie_list=list(list_reader)

d.get('https://movie.naver.com/')

for movie in movie_list:
    title=movie[0]
    genre=movie[1]

    movie_input=d.find_element_by_xpath('//*[@id="ipt_tx_srch"]')
    d.execute_script('''
        var movie_input=arguments[0];
        var value=arguments[1];
        movie_input.value=value;
        ''', movie_input, title)
    d.find_element_by_xpath('//*[@class="btn_srch"]').click()
    sleep(2)
    d.find_element_by_xpath('//*[@class="search_list_1"][1]/li[1]/p/a').click()
    sleep(3)

    # 리뷰 페이지로 이동
    d.find_element_by_xpath('//*[@class="tab05_off"]').click()

    movie_title=d.find_element_by_xpath('//*[@class="mv_info_area"]/div[@class="mv_info"]/h3/a[1]').text
    print(movie_title)
    movie_title.replace(":", "_")

    #csvfile 만들기
    with open('./review_{}_{}.csv'.format(genre, movie_title), 'w', encoding='utf8') as csvfile:
        fieldnames=["score", "review", "time", "released", "genre"]
        writer=csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

    # 개봉 후 평점 받아오기, 한 페이지에 열 개
    # page 내부, 네티즌 댓글 전용 iframe 들어가기
    d.switch_to.frame("pointAfterListIframe")
    page_num=get_page_num()
    get_reviews(page_num, True, genre)

    #개봉 전 받아오기
    d.switch_to.default_content()
    d.find_element_by_xpath('//*[@id="beforePointTab"]/a').click()

    d.switch_to.frame("pointAfterListIframe")
    page_num2=get_page_num()
    get_reviews(page_num2, False, genre)

    # 기본으로 되돌리기
    d.switch_to.default_content()


# d.get('https://movie.naver.com/movie/bi/mi/basic.nhn?code=167638') #167638


d.quit()
