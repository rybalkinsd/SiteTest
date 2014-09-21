import logging
from selenium import webdriver
import re
import sys
# url could be google.com/bla-bla/ref=http://new.sportmaster...


target_web_app = re.compile('^htt(p|ps)://new\\.sportmaster\\.ru')

# continue param and login/logout
restrictions = ["login", "logout", "continue="]

#root url
main_url = "http://new.sportmaster.ru"

#logger init
logger = logging.getLogger('SiteTest')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def main():
    logger.info("start")
    try:
        browser = webdriver.Chrome()
        browser.get(main_url)
    except Exception:
        logger.error("Browser initialize error " + main_url)
        return

    url_story = []
    url_queue = [main_url]

    while len(url_queue):
        logger.info("Url in story: " + str(len(url_story)) + ". Url in queue: " + str(len(url_queue)))
        url = url_queue.pop()
        find_urls(url, browser, url_story, url_queue)
        save_urls(url_story)

    browser.close()


    logger.log("finish")


def find_urls(root_url, browser, url_story, url_queue):
    try:
        browser.get(root_url)
        list_tags = browser.find_elements_by_tag_name('a')
    except:
        logger.error("Url opening timeout")
        return

    try:
        leaf_urls = [item.get_attribute('href') for item in list_tags]
        # filter
        leaf_urls = list(filter(lambda x: x is not None
                                      and is_not_restricted(x, restrictions), leaf_urls))

        for url in leaf_urls:
            if url not in url_story:
                url_story.append(url)
                if target_web_app.match(url):
                    url_queue.append(url)
    except:
        logger.error("Descriptor format error")
        return

def is_not_restricted(target, restrictions):
    for restriction in restrictions:
        if restriction in target: 
            return False

    return True

def save_urls(urls):
    logger.info("saving urls")
    with open('urls.txt', 'w') as file_:
        for url in urls:
            file_.write(url + "\n")


if __name__ == "__main__":
    main()