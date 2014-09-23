#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver

def match_errors(browser, logger):
    list_title = browser.find_elements_by_tag_name('title')
    if match_title(list_title):
        logger.error(u'Ушли на перерыв in title {0}'.format(browser.current_url))
        return True

    list_h1 = browser.find_elements_by_tag_name('h1')
    if match_h1(list_h1):
        logger.error(u'Страница не найдена in h1 {0}'.format(browser.current_url))
        return True


def match_title(titles):
    for title in titles:
        if u'Ушли на перерыв' in title.text:
            return True

    return False

def match_h1(h1s):
    for h1 in h1s:
        if u'Страница не найдена' in h1.text:
            return True

    return False