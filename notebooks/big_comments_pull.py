import praw
from _secrets import user_agent, client_id, client_secret
import pandas as pd
from tqdm import tqdm

reddit = praw.Reddit(user_agent='Update Comments Corpus, /u/Holden-McRoyne',
                     client_id=client_id,
                     client_secret=client_secret)

submissions = pd.read_csv('../data/submissions.csv')['id']
comments = pd.read_csv('../data/comments.csv')

submissions = [reddit.submission(id=Id) for Id in pd.read_csv('../data/submissions.csv')['id']]

df=pd.DataFrame()
for submission in tqdm(submissions):
    comments_tree = submission.comments
    comments_tree.replace_more(limit=0)
    df.append(pd.DataFrame([c.__dict__ for c in comments_tree]))

df.to_csv('comments.csv')