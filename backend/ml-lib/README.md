## Machine Learning Libraries
Automated modules with clustering and NLP.

Contains:
- 'HyperML' pipeline for reading data, pre-processing, prediction, evaluation.
- Sentiment Analysis for policy type weighing.
- Text Generator for AGVN blog post style action/policy generation.
- Text Summarizer for department analysis and extraction of key themes, e.g. policy types/synonyms for sentiment analysis.

## HyperML
![](HyperML-3.png)

Machine Learning pipeline for main processing of political interests into Initiatives. Aggregates user data into blocks and matches an 'ideology' to each group of users.

Initiatives are generated from ideological reweighing based on past election term's polling data and sentiment data from the internet.

In the [API](ml_api.py), the functions are used for the [ML microservice](server.py) consumed by the main webserver.

## Extensions
- attach sentiment analyzer to analyze each day's sentiment for past 30 days
- look at the word list for synonyms that match a policy topic
    - for each word, see whether it has a >70% match (nltk) with a policy topic
    - if match, count+=match
    - if match > 3 (arbitrary), then high probability that the day's sentiment matches this policy topic
    - adjust the weights (add) by the sentiment value divided by 10
