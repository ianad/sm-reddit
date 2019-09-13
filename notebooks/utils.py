import praw
from _secrets import default_user_agent, client_id, client_secret
import pandas as pd
from tqdm import tqdm
import numpy as np
import random


def initialize_reddit(user_agent = default_user_agent):
    reddit = praw.Reddit(user_agent = user_agent,
                        client_id = client_id,
                        client_secret = client_secret)
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

    
def jargon_score(obj):
    # Try to cast 'obj' as numpy array
    try: array_obj = np.array(obj).astype('str')
    except: TypeError(f"`obj` should be castable as NumPy array-like of strings, not {type(obj)}")
    
    # Another test: `obj` should also be 1-dimensional
    if array_obj.ndim != 1:
        raise ValueError("`obj` should be 1-dimensional")
    
    # placeholder dictionary
    english_dictionary = ['a', 'the', 'but', 'yes', 'no', 'fizz', 'buzz', 'hello', 'world', 'quick', 'brown', 'fox']
        
    # defining Rules as lambda functions in a list so len(ruleset) can be referenced later
    # each returning a boolean value cast as a float to allow for later weighting
    ruleset = (
        lambda token: float(str.isupper(token[0])), # first letter in token is capitalized
        lambda token: float(token not in english_dictionary), # token is not an english word
    )

    # Create dummy scores object 
    # Should be 2 dimensional 
    ## dim_1 = len(array_obj) 
    ## dim_2 = len(ruleset)
    all_scores = np.empty(
        (array_obj.shape[0],
         len(ruleset))
    )
    
    

    for t, token in enumerate(array_obj):
        for r, rule in enumerate(ruleset):
            score = rule(token)
            # apply each rule lambda in `ruleset` to each token in `array_obj`
            all_scores[t,r] = score
            pass
    
    # Mean out all the scores and return a 1-dimensional array same shape with `obj`
    scores = np.array([v.mean() for v in all_scores])
    return(scores)

def praw2series(praw_obj, filter=False):
       
    try:
        praw_obj.name
    except:
        raise Warning(f'Encountered an error querying the {type(praw_obj)} model.')
    else:
        obj_dict = praw_obj.__dict__

    if filter:
        # filter out the praw objects in the series
        raise Warning(f'Filtering not implemented.')
    
    return(obj_dict)

def sample_subreddit():
    reddit = initialize_reddit(user_agent='Sample subreddit getter')
    
    subreddit_name = pd.read_csv('../data/subreddits.csv')['display_name'].sample(1)
    subreddit_name = subreddit_name[subreddit_name.index[0]]

    random_subreddit = reddit.subreddit(subreddit_name)
    return(random_subreddit)

def sample_submission(from_subreddit=None):
    reddit = initialize_reddit(user_agent='Sample submission getter')
    
    if from_subreddit: # is specified
        subreddit = reddit.subreddit(from_subreddit)
    else:
        subreddit = sample_subreddit()

    random_submission = subreddit.random()

    return(random_submission)

def sample_comment(from_subreddit=None, from_submission=None):
    reddit = initialize_reddit(user_agent='Sample comment getter')

    if from_submission: # is specified
        submission = reddit.submission(from_submission)
    if from_subreddit: # is specified
        submission = sample_submission(from_subreddit)
    else:
        submission = sample_submission()
        
    comments = []
    while len(comments) < 1:
        try:
            comments = [c for c in submission.comments]
        except AttributeError:
            pass
    
    random_comment = random.choice(comments)
    return(random_comment)
