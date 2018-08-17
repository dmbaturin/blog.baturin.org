#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Daniil Baturin'
SITENAME = "dmbaturin's blog"
SITEURL = 'https://blog.baturin.org'

PATH = 'content'

TIMEZONE = 'Etc/UTC'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('dmbaturin\'s website', 'http://baturin.org/'),
         ('VyOS project', 'https://www.vyos.io/'))

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

STATIC_PATHS = ['images']

PIWIK_URL = 'matomo.baturin.org'
PIWIK_SITE_ID = 'blog.baturin.org'

DISQUS_SITENAME = 'blog-baturin-org'
