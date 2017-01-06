import sys
import json
from collections import Counter


def read_tweets(filename):
    tweets = []
    with open(filename) as f:
        for line in f.readlines():
            data = json.loads(line)
            tweets.append(data)
    return tweets


def get_hashtags(tweet):
    try:
        return [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
    except KeyError:
        return []


def main():
    tweets = read_tweets(sys.argv[1])

    hashtag_counts = Counter()
    for tweet in tweets:
        hashtag_counts.update(get_hashtags(tweet))

    for hashtag, count in hashtag_counts.most_common(10):
        print hashtag, count


if __name__ == '__main__':
    main()
