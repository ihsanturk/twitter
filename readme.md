# Twitter Scraper & Streamer

[![built with nix](https://builtwithnix.org/badge.svg)](https://builtwithnix.org)

## Install
```
git clone https://gitlab.com/ihsanturk/twitter && cd twitter
curl -L https://nixos.org/nix/install | sh
nix-shell
```
Now you are in a subshell that makes twitter cli available.

## Use
```sh
twitter --help
```

## Notes for Developer
Some of the meanings in the source code;
- `#TODO#<number>`: A thing to do with enumarated priority. For example #TODO#0 means first problem to solve (do). #TODO#1 is a problem that needs to be solved after #TODO#0 solved.
- `#TODO#p`: A thing to do when going production.
- `#TODO#e`: A thing to do at the end of the project. After solving everything before.
- `#TODO#c`: A thing to do before a git commit.

### Twint Tweet Object
```
[<class 'str'>]: id_str: 1322510370129457152
[<class 'str'>]: conversation_id: 1322510370129457152
[<class 'str'>]: datetime: 2020-10-31 15:06:57 +03
[<class 'str'>]: datestamp: 2020-10-31
[<class 'str'>]: timestamp: 15:06:57
[<class 'int'>]: user_id: 447465481
[<class 'str'>]: user_id_str: 447465481
[<class 'str'>]: username: engincevirgen
[<class 'str'>]: name: Engin CEVIRGEN
[<class 'str'>]: place:
[<class 'str'>]: timezone: +0300
[<class 'list'>]: mentions: []
[<class 'list'>]: urls: []
[<class 'list'>]: photos: []
[<class 'int'>]: video: 0
[<class 'str'>]: thumbnail:
[<class 'str'>]: tweet: 😁🇹🇷  #xu100 #xu50 #xu30 #aefes #goody #icbct #thyao #türkiye
[<class 'str'>]: lang: und
[<class 'list'>]: hashtags: ['xu100', 'xu50', 'xu30', 'aefes', 'goody', 'icbct', 'thyao', 'türkiye']
[<class 'list'>]: cashtags: []
[<class 'int'>]: replies_count: 0
[<class 'int'>]: retweets_count: 0
[<class 'int'>]: likes_count: 0
[<class 'str'>]: link: https://twitter.com/engincevirgen/status/1322510370129457152
[<class 'str'>]: quote_url: https://twitter.com/iriscibre/status/1322499018098921472
[<class 'str'>]: near:
[<class 'str'>]: geo:
[<class 'str'>]: source:
[<class 'dict'>]: reply_to: {'user_id': None, 'username': None}
[<class 'str'>]: translate:
[<class 'str'>]: trans_src:
[<class 'str'>]: trans_dest:
[<class 'int'>]: _id: 1322510370129457152
```

