from selenium import webdriver
import re

# url could be google.com/bla-bla/ref=http://new.sportmaster...
target_web_app = re.compile('^htt(p|ps)://new\\.sportmaster\\.ru')

# continue param and login/logout
restrictions = ["login", "logout","continue="]

#root url
main_url = "http://new.sportmaster.ru"


def testSite():
    print("start")
    browser = webdriver.Chrome()
    browser.get(main_url)

    url_story = []
    url_queue = [main_url]

    while len(url_queue):
        print("url story size: ", len(url_story), " url queue: ", len(url_queue))
        url = url_queue.pop()
        find_urls(url, browser, url_story, url_queue)

    browser.close()

    save_urls(url_story)
    print("end")


def find_urls(root_url, browser, url_story, url_queue):
    browser.get(root_url)
    list_tags = browser.find_elements_by_tag_name('a')
    leaf_urls = [item.get_attribute('href') for item in list_tags]

    # filter
    leaf_urls = list(filter(lambda x: x is not None
                                  and is_not_restricted(x, restrictions), leaf_urls))

    for url in leaf_urls:
        if url not in url_story:
            url_story.append(url)
            if target_web_app.match(url):
                url_queue.append(url)

def is_not_restricted(target, restrictions):
    for restriction in restrictions:
        if restriction in target: 
            return False

    return True

def save_urls(urls):
    with open('urls.txt', 'w') as file_:
        for url in urls:
            file_.write(url + "\n")
        print(file_.name)



testSite()