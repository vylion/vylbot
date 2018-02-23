#!/usr/bin/env python3

def parse_line(l):
    s = l.split('=')
    if len(s) < 2:
        return ""
    else:
        return s[1]

class ChatReader(object):
    def __init__(self, cid, ctype, title):
        self.id = str(cid)
        self.type = ctype
        self.title = title
