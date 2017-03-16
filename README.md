# retweet_counter
Get current retweet count and send result mail.

## Command
```sh
python retweet_counter.py --mail to@hoge.com --tweetid 836446157698052096 833829909126475776 --subject "Hello, world"
```

## Mail sample

```
https://twitter.com/i/web/status/836446157698052096
====================
2017/03/16 16:11:39, 0
2017/03/16 16:11:45, 0

https://twitter.com/i/web/status/833829909126475776
====================
2017/03/16 16:11:39, 1
2017/03/16 16:11:45, 1
```
