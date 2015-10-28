#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'elpatron'
# derived from https://github.com/mattermost/mattermost-integration-gitlab

import requests
import json
import feedparser
import time
from rssfeed import RssFeed

mattermost_webhook_url = 'https://192.168.0.238/hooks/cns14rjjfpfrxpgoujxpm7sy3w'  # Paste the Mattermost webhook URL you created here
mattermost_channel = 'testing'  # Leave this blank to post to the default channel of your webhook

# Your feeds come here:
# RssFeed('Feed name', 'Feed URL', 'Mattermost username', 'Mattermost channel')
feeds = {RssFeed('Heise News', 'http://heise.de.feedsportal.com/c/35207/f/653902/index.rss', 'RSS-Bot', 'testing'),
         RssFeed('t3n', 'https://feeds2.feedburner.com/aktuell/feeds/rss/', 'RSS-Bot', 'testing')
         }


def post_text(text, username, channel):
    """
    Mattermost POST method, posts text to the Mattermost incoming webhook URL
    """

    data = {}
    data['text'] = text
    if len(username) > 0:
        data['username'] = username
    if len(channel) > 0:
        data['channel'] = channel

    headers = {'Content-Type': 'application/json'}
    r = requests.post(mattermost_webhook_url, headers=headers, data=json.dumps(data), verify=False)

    if r.status_code is not requests.codes.ok:
        print('Encountered error posting to Mattermost URL %s, status=%d, response_body=%s' % (mattermost_webhook_url, r.status_code, r.json()))


if __name__ == "__main__":
    if len(mattermost_webhook_url) == 0:
        print('MATTERMOST_WEBHOOK_URL must be configured. Please see instructions in README.md')
        sys.exit()

    while 1:
        for feed in feeds:
            d = feedparser.parse(feed.url)
            feed.newtitle = d['entries'][0]['title']
            feed.articleurl = d['entries'][0]['link']

            if feed.lasttitle != feed.newtitle:
                print(feed.url)
                print('Title: ' + feed.newtitle + '\n')
                print('Link: ' + feed.articleurl + '\n')
                # description = d['entries'][0]['content'][0]
                feedtext = feed.name + ': ' + feed.newtitle + ' (' + feed.articleurl + ')'
                post_text(feedtext, feed.user, feed.channel)
                feed.lasttitle = feed.newtitle
            else:
                print('Nothing new. Waiting for good news...')

        time.sleep(60)


