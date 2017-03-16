# -*- coding: utf-8 -*-
"""
Get retweet count and send result mail.
"""
import sys
sys.path.insert(0, 'libs')

import argparse
import datetime
import os
import tweepy
import xmlrpclib


root = os.path.abspath(os.path.dirname(__file__))

tweet_id_description_fmt = u"""
https://twitter.com/i/web/status/{}
====================
"""

def send_simple_mail(send_from, send_to, send_cc, subject, body):
    proxy = xmlrpclib.ServerProxy('') # <= Mail server
    proxy.send(send_from, send_to, send_cc, '', subject, body)

class Tw:
    def __init__(self):
        consumer_key = ''
        consumer_secret = ''
        oauth_token = ''
        oauth_token_secret = ''

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(oauth_token, oauth_token_secret)
        self.api = tweepy.API(auth_handler=auth)

    def get_tweet_info_by_tweet_id(self, tweet_id):
        status = self.api.get_status(tweet_id)
        print "TweetID:", tweet_id

        return status

def output_logfile(tweet_ids):
    tw = Tw()

    now = datetime.datetime.now()
    t = now.strftime('%Y/%m/%d %H:%M:%S')
    for tweet_id in tweet_ids:
        status = tw.get_tweet_info_by_tweet_id(tweet_id)
        filepath = os.path.join(root, 'retweet_{}.csv'.format(str(tweet_id)))

        with open(filepath, 'a') as f:
            f.write("{}, {}\n".format(t, str(status.retweet_count)))


        result = tweet_id_description_fmt.format(tweet_id)
        with open(filepath, 'r') as f:
            for line in f:
                day, count = line.strip().split(',')
                result += u"{}: Retweet{}\n".format(day, count)


def send_result(tweet_ids, args):
    message = ""
    for tweet_id in tweet_ids:
        filepath = os.path.join(root, 'retweet_{}.csv'.format(str(tweet_id)))
        if os.path.exists(filepath):
            message += tweet_id_description_fmt.format(tweet_id)
            with open(filepath, 'r') as f:
                message += f.read()

    if message:
        send_simple_mail('SEND-ONLY@hoge.com',
                         ','.join(args.mails),
                         ','.join(args.cc),
                         args.subject,
                         message)
    else:
        print "No message."


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""
    Get retweet count from tweet id and send result by mail.
    """)
    parser.add_argument('-M', '--mail', dest='mails', nargs='+',
                        help='Email address to send result mail.')

    parser.add_argument('--cc', dest='cc', nargs='+',
                        help='CC address to send result mail.')

    parser.add_argument('-T', '--tweetid', dest='tweetids', nargs='+',
                        help='''
                        Tweet ids.
                        https://twitter.com/i/web/status/[XXXXXXXXXXXXXXXXXXXXXXX] <-
                        ''')

    parser.add_argument('-S', '--subject', dest='subject', default="[Retweet counter]",
                        help='''
                        Mail subject.
                        ''')
    args = parser.parse_args()

    output_logfile(args.tweetids)
    send_result(args.tweetids, args)

