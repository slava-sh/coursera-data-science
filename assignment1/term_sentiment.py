import re
import sys
import json
from collections import defaultdict


def read_scores(filename):
    scores = {}
    with open(filename) as f:
        for line in f.readlines():
            term, score = line.split("\t")
            scores[term] = int(score)
    return scores


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


def get_tweet_sentiment_score(tweet, scores):
    total_score = 0
    terms = get_terms(tweet)
    if not terms:
        return 0
    for term in terms:
        total_score += scores.get(term, 0)
    return float(total_score) / len(terms)


def get_new_scores(tweets, scores):
    total_scores = defaultdict(float)
    occurence_counts = defaultdict(int)
    for tweet in tweets:
        tweet_score = get_tweet_sentiment_score(tweet, scores)
        for term in get_terms(tweet):
            if term in scores:
                continue
            total_scores[term] += tweet_score
            occurence_counts[term] += 1

    new_scores = {}
    for term, total_score in total_scores.items():
        new_scores[term] = total_score / occurence_counts[term]
    return new_scores


def main():
    scores = read_scores(sys.argv[1])
    tweets = read_tweets(sys.argv[2])
    new_scores = get_new_scores(tweets, scores)
    for term, score in new_scores.items():
        print term, score


if __name__ == '__main__':
    main()
