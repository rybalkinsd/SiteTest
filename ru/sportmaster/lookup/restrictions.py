# continue param and login/logout
import re

restrictions = [
    re.compile('.*login.*'),
    re.compile('.*logout.*'),
    re.compile('.*continue=.*'),
    re.compile('.*facetValues.*facetValues.*')
]


def is_not_restricted(target):
    for restriction in restrictions:
        if restriction.match(target):
            return False

    return True
