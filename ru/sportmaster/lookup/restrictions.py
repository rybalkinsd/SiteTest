# continue param and login/logout
import re

# standard restrioctions to all url BFS
# restrictions = [
#     re.compile('.*login.*'),
#     re.compile('.*logout.*'),
#     re.compile('.*continue=.*'),
#     re.compile('.*facetValues.*facetValues.*')
# ]

# exclude all facets and catalog
restrictions = [
    re.compile('.*login.*'),
    re.compile('.*logout.*'),
    re.compile('.*continue=.*'),
    re.compile('.*facetValues.*'),
    re.compile('^htt(p|ps)://new.staging\.testim\.sportmaster\.ru/catalog.*')
]


def is_not_restricted(target):
    for restriction in restrictions:
        if restriction.match(target):
            return False

    return True
