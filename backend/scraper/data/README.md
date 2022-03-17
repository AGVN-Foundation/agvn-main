## Sentiment Data
Literally just a folder filled with jsons of sentiment collected each each day.
Sentiments are basically any social media post, comment, news article.
They are stored separately as strings.

- We do our best to 'normalize' the data by removing 'unnecessary' things. And we only scrape text bodies, not the entire article.
- Each article type, e.g. SMH, etc. requires some distinct 'scraping techniques' to ensure only text is scraped.
- If it is too hard to scrape page texts distinctically, GPT-2 will be used to summarize an entire HTML article. All tags will be removed.

## Raw vs Sentiment
Raw data is the actual raw data scraped from the internet.
It is stored in mongodb like the example [`raw-2021-01-01.json`](raw-2021-01-01.json).

Sentiment data is simply a list of strings with the most frequent words that is expressed.
Words like 'the, a' and other 'grammar words' will not be considered. Algorithms may be hardcoded to ensure those 'nonwords' are not included.
Sentiment data is simply stored as JSON object-lists marked by their date. The table of all sentiments is exemplified in [`sentiment.json`](sentiment.json).

Sentiment data is automatically normalized, removing all punctuation and making everything lowercase.

#### How to adjust Sentiment Data
If you wish to test how everything sentiment related will work out,
it is imperative to be able to change sentiments manually on the fly.

The server on [`/scraper`](../server.py) allows us to send a bunch of custom sentiment data for a current date in.

We can send anything relevant like:
```
{
"2021-01-01": [
        "angry", "ill", "believe"
    ]
},
"2021-01-02": [
        "angry", "ill", "believe"
    ]
},
"2021-01-03": [
        "angry", "ill", "believe"
    ]
},
...
"2021-01-30": [
        "angry", "ill", "believe"
    ]
},
}
```

The ML libs take from the past 30 days. If the sentiment is the same for the previous 30 days, it will be able to figure out that a key sentiment is "ill" which matches with the policy type "health"
It will then use GPT to generate a poll question based on the prompt

