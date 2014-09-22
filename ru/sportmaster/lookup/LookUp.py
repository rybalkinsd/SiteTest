from selenium import webdriver
import re

from ru.sportmaster.lookup.TimeoutDecorator import timeout
from ru.sportmaster.lookup.Restrictions import is_not_restricted
from ru.sportmaster.lookup.LoggerUtils import getLogger


# url could be google.com/bla-bla/ref=http://new.sportmaster...
target_web_app = re.compile('^htt(p|ps)://new\\.sportmaster\\.ru')

#root url
main_url = "http://new.sportmaster.ru"

logger = getLogger()

def main():
    logger.info("start")
    try:
        browser = webdriver.Chrome()
        browser.get(main_url)
    except Exception:
        logger.error("Browser initialize error: " + main_url)
        return

    url_story = []
    url_queue = [main_url]

    while len(url_queue):
        logger.info("Url in story: " + str(len(url_story)) + ". Url in queue: " + str(len(url_queue)))

        url = url_queue.pop()
        try:
            find_urls(url, browser, url_story, url_queue)
        except:
            logger.error("Time limit processing url: " + url)

        save_urls(url_story)

    browser.close()

    logger.info("finish")


@timeout(7)
def find_urls(root_url, browser, url_story, url_queue):
    try:
        browser.get(root_url)
        list_tags = browser.find_elements_by_tag_name('a')
    except:
        logger.error("Can't open url: " + root_url)

    try:
        leaf_urls = [item.get_attribute('href') for item in list_tags]
        # filter
        leaf_urls = list(filter(lambda x: x is not None
                                      and is_not_restricted(x), leaf_urls))

        for url in leaf_urls:
            if url not in url_story:
                url_story.append(url)
                if target_web_app.match(url):
                    url_queue.append(url)
    except:
        logger.error("Descriptor format error")
        return

def save_urls(urls):
    logger.info("saving urls")
    with open('urls.txt', 'w') as file_:
        for url in urls:
            file_.write(url + "\n")


if __name__ == "__main__":
    main()