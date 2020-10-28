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
