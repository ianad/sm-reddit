import praw
from _secrets import user_agent, client_id, client_secret
import pandas as pd
from tqdm import tqdm

def initialize_reddit(agent_string = user_agent):
    reddit = praw.Reddit(user_agent = agent_string,
                        client_id=client_id,
                        client_secret=client_secret)
    return(reddit)


def initialize_model(reddit, model_type, *args, **kwargs):
    assert type(reddit) == praw.reddit.Reddit
    if type(model_type) == str:
        model_func = getattr(reddit, model_type)
    model = model_func(*args, **kwargs)
    try:
        model.name
    except:
        raise Warning(f'Encountered an error querying the {type(model)} model.')
    return(model)

def big_comments_pull():
    reddit = initialize_reddit('Update Comments Corpus, /u/Holden-McRoyne')

    submissions = pd.read_csv('../data/submissions.csv')['id']
    comments = pd.read_csv('../data/comments.csv')

    submissions = [reddit.submission(id=Id) for Id in pd.read_csv('../data/submissions.csv')['id']]

    df=pd.DataFrame()
    for submission in tqdm(submissions):
        comments_tree = submission.comments
        comments_tree.replace_more(limit=0)
        df.append(pd.DataFrame([c.__dict__ for c in comments_tree]))

    df.to_csv('comments.csv')