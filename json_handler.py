import json
import sys

# GHARCHIVE QUERIES
# Program to query gharchive data (json format)
# Current implementation searches for term stored in msg_search
# and returns list of resulting github url, commit hash, and repo name


def sanitize(url, msg):
    lst = url.split("/commits/")
    l = len(lst[0])
    temp = lst[0].split("/")
    repo = temp[5]
    lst[0] = "https://github.com" + lst[0][28:l] + ".git"
    lst += [repo]
    lst += [''.join(i for i in msg if ord(i)<128)]
    return tuple([str(x) for x in lst])


def get_urls(filename, msg_search, event_search):
    with open(filename) as f:
        data = [json.loads(line) for line in f]
        payloads = [x['payload'] for x in data if x['type'] == event_search]
        # payloads = [x['payload'] for x in data]
        commits = [y['commits'][i] for y in payloads if 'commits' in y for i in range(len(y['commits']))]
        return str([sanitize(z['url'], z['message']) for z in commits if 'message' in z and msg_search in z['message']])


fn = sys.argv[1]
msg_srch = sys.argv[2]
evnt_srch = sys.argv[3]
print(get_urls(fn, msg_srch, evnt_srch))
# print(get_urls("2015-01-01-15.json", "null", "PushEvent"))