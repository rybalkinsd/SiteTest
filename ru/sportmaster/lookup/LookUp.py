from Queue import Queue
from selenium import webdriver
import re

from LoggerUtils import getFileLogger, getStreamLogger
from restrictions import is_not_restricted

from TimelimitWindows import call_with_time_limit
from ErrorFinder import match_errors

target_web_app = \
    re.compile('^htt(p|ps)://new\\.staging\\.testim\\.sportmaster.ru/')
    # re.compile('^htt(p|ps)://localhost:(8080|8443)/war-sportmaster/')
    # re.compile('^htt(p|ps)://new\\.sportmaster\\.ru')

#root url
main_url = "http://new.staging.testim.sportmaster.ru/"

workflow_log = getFileLogger('workflowLog.log')
reached_url_log = getFileLogger('reached_url.log')
story_log = getFileLogger('story_url.log')
std_log = getStreamLogger()

time_limit = 30

def main():
    std_log.info("start")
    try:
        browser = webdriver.Chrome()
    except:
        workflow_log.error("Browser initialize error: {0}".format(main_url))
        return

    found_urls = set()
    found_urls_reached = set()
    look_up_story = set()
    url_queue = Queue()
    url_queue.put(main_url)

    while not url_queue.empty():
        std_log.info("Iteration #{0!s}".format(len(look_up_story)))
        workflow_log.info("Url in story: {0!s}. Url in queue: {1!s}".format(len(found_urls), url_queue.qsize()))

        # renew browser to prevent fatal error
        if len(look_up_story) % 50 == 0:
            std_log.info("Chrome browser renew")
            workflow_log.info("Chrome browser renew")
            browser.quit()
            browser = webdriver.Chrome()

        root_url = url_queue.get()
        look_up_story.add(root_url)
        story_log.info(root_url)

        workflow_log.info("Processing url: {0}".format(root_url))

        reached_urls = None
        internal_urls = None

        try:
            reached_urls, internal_urls = \
                call_with_time_limit(time_limit, find_urls, (root_url, browser))
        except:
            std_log.error("Time limit expired, url: {0}".format(root_url))
            workflow_log.error("Time limit expired, url: {0}".format(root_url))

        if reached_urls is not None:
            for url in reached_urls:
                if url not in found_urls_reached:
                    found_urls.add((url, root_url))
                    found_urls_reached.add(url)
                    log_url((url, root_url))

        if internal_urls is not None:
            for url in internal_urls:
                if url not in look_up_story \
                        and url not in url_queue.queue:
                    url_queue.put(url)

    browser.quit()
    std_log.info("finish")


def find_urls(root_url, browser):
    try:
        browser.get(root_url)
        match_errors(browser, workflow_log)

        list_tags = browser.find_elements_by_tag_name('a')
    except:
        workflow_log.error("Can't open url: {0}".format(root_url))
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
        workflow_log.error("Descriptor format error")
        return


def log_url(url):
    reached_url_log.info("@reached {0[0]} @from: {0[1]}".format(url))


if __name__ == "__main__":
    main()