import re
import sys
import json
from collections import defaultdict


def read_tweets(filename):
    tweets = []
    with open(filename) as f:
        for line in f.readlines():
            data = json.loads(line)
            tweets.append(data)
    return tweets


TERMS_RE = re.compile('\w+')


def get_terms(tweet):
    try:
        text = tweet['text']
    except KeyError:
        return []
    terms = TERMS_RE.findall(text)
    terms = [term.lower() for term in terms]
    return terms


def get_term_frequences(tweets):
    term_counts = defaultdict(int)
    total_count = 0
    for tweet in tweets:
        for term in get_terms(tweet):
            term_counts[term] += 1
            total_count += 1

    frequencies = {}
    for term, count in term_counts.items():
        frequencies[term] = float(count) / total_count
    return frequencies


def main():
    tweets = read_tweets(sys.argv[1])
    frequencies = get_term_frequences(tweets)
    for term, frequency in frequencies.items():
        print term, frequency


if __name__ == '__main__':
    main()
