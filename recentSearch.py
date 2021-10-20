import requests
import os
import json
import sqlite3

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")

search_url = "https://api.twitter.com/2/tweets/search/recent"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
# there are some other metrics as well but not allowed to access it currently
query_params = {
    # "query": "(from:twitterdev -is:retweet) OR #twitterdev",
    "query": "ethereum",
    # "tweet.fields": "author_id",
    "tweet.fields": "author_id,attachments,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld",
}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    response = connect_to_endpoint(search_url, query_params)
    # print(json.dumps(response, indent=4, sort_keys=True))
    # print(f"response {type(response)}")

    conn = sqlite3.connect("tweets.db")
    cur = conn.cursor()
    cur.execute(
        """
                CREATE TABLE IF NOT EXISTS Tweets(id VARCHAR, tweet TEXT, data JSON)"""
    )
    for twt in response["data"]:
        cur.execute(
            "INSERT INTO Tweets (id, tweet, data) VALUES (?, ?, ?)",
            (twt["id"], twt["text"], json.dumps(twt)),
        )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
