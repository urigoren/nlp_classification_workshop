# Accuracy Service
## Why am I seeing a php folder in a python workshop ?

The source code in this directory has nothing to do with the contents of the NLP workshop.

This PHP code serves as our accuracy service, that ranks, stores, and views submissions and their scores.

The PyData TLV website is powered by `Wordpress` (written in `PHP`) and this service is designed to run side by side with our website (`www.pydata.org.il`).

Do not be offended, we love python, but we are also pragmatic and choose the tools that help us achieve our goals fastest.

## Deployment
1. Create a `{"example":"label"}` mapping, and save it in `json` format as `truth.data`
1. Upload both `truth.data` and `server.php` to your website root directory.

## Usage
1. A request with both an `user` and a `submission` field is recorded.
1. The format of the `submission` field should be a `json` mapping of `{"example":"label"}` (same as `truth.data`)
1. Any other request, is routed to the leaderboard.
