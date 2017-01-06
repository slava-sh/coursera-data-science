import re
import sys
import json
from collections import defaultdict

states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AS': 'American Samoa',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MP': 'Northern Mariana Islands',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NA': 'National',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VI': 'Virgin Islands',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}


def get_state_code(tweet):
    try:
        location = tweet['user']['location']
    except KeyError:
        return None
    if not location:
        return None
    for state_code, state_name in states.items():
        state_code_re = re.compile(r'\b{}\b'.format(re.escape(state_code)))
        state_name_re = \
            re.compile(r'\b{}\b'.format(re.escape(state_name)), re.IGNORECASE)
        if state_code_re.match(location) or state_name_re.match(location):
            return state_code
    return None


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


def get_scores_for_states(tweets, scores):
    total_scores = defaultdict(float)
    occurence_counts = defaultdict(int)
    for tweet in tweets:
        state_code = get_state_code(tweet)
        if not state_code:
            continue
        tweet_score = get_tweet_sentiment_score(tweet, scores)
        total_scores[state_code] += tweet_score
        occurence_counts[state_code] += 1

    state_scores = {}
    for state_code, total_score in total_scores.items():
        state_scores[state_code] = total_score / occurence_counts[state_code]
    return state_scores


def main():
    scores = read_scores(sys.argv[1])
    tweets = read_tweets(sys.argv[2])
    scores = get_scores_for_states(tweets, scores)

    happiest_state = None
    for state_code, score in scores.items():
        if happiest_state is None or score > scores[happiest_state]:
            happiest_state = state_code
    print happiest_state


if __name__ == '__main__':
    main()
