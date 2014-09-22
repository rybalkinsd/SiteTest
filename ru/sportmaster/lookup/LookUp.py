from Queue import Queue
from selenium import webdriver
import re

from LoggerUtils import getLogger
from restrictions import is_not_restricted

from TimelimitWindows import call_with_time_limit
from ErrorFinder import match_errors

target_web_app = \
    re.compile('^htt(p|ps)://new.staging.testim.sportmaster.ru/')
    # re.compile('^htt(p|ps)://localhost:(8080|8443)/war-sportmaster/')
    # re.compile('^htt(p|ps)://new\\.sportmaster\\.ru')

#root url
main_url = "http://new.staging.testim.sportmaster.ru/"
logger = getLogger()
time_limit = 10

def main():
    logger.info("start")
    try:
        browser = webdriver.Chrome()
    except:
        logger.error("Browser initialize error: " + main_url)
        return

    url_story = []

    url_queue = Queue()
    url_queue.put(main_url)

    while not url_queue.empty():
        logger.info("Url in story: " + str(len(url_story)) + ". Url in queue: " + str(url_queue.qsize()))

        root_url = url_queue.get()
        logger.info("Processing url: " + root_url)

        reached_urls = None
        internal_urls = None

        try:
            reached_urls, internal_urls = \
                call_with_time_limit(time_limit, find_urls, (root_url, browser))
        except:
            logger.error("Time limit expired, url: " + root_url)

        if reached_urls is not None:
            for url in reached_urls:
                if url not in url_story:
                    url_story.append((url, root_url))

        if internal_urls is not None:
            for url in internal_urls:
                if url not in url_queue.queue:
                    url_queue.put(url)

        save_urls(url_story)

    browser.close()
    logger.info("finish")


def find_urls(root_url, browser):
    try:
        browser.get(root_url)
        match_errors(browser, logger)

        list_tags = browser.find_elements_by_tag_name('a')
    except:
        logger.error("Can't open url: " + root_url)
        return

    try:
        reached_urls = [item.get_attribute('href') for item in list_tags]
        # filter
        reached_urls = list(filter(lambda x: x is not None
                                      and is_not_restricted(x), reached_urls))

        internal_urls = []
        for url in reached_urls:
            if target_web_app.match(url):
                internal_urls.append(url)

        return reached_urls, internal_urls
    except:
        logger.error("Descriptor format error")
        return




def save_urls(urls):
    logger.info("saving urls")
    with open('urls.txt', 'w') as file_:
        for url in urls:
            file_.write(url[0] +" from: " + url[1] + "\n")


if __name__ == "__main__":
    main()