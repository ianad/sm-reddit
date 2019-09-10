import praw
from _secrets import user_agent, client_id, client_secret
import pandas as pd
from tqdm import tqdm
import numpy as np



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

    
def jargon_score(obj):
    # Try to cast 'obj' as numpy array
    try: array_obj = np.array(obj).astype('str')
    except: TypeError(f"`obj` should be castable as NumPy array-like of strings, not {type(obj)}")
    
    # Another test: `obj` should also be 1-dimensional
    if array_obj.ndim != 1:
        raise ValueError("`obj` should be 1-dimensional")
    
    # placeholder dictionary
    english_dictionary = ['a', 'the', 'but', 'yes', 'no', 'fizz', 'buzz', 'hello', 'world']
        
    # defining Rules as lambda functions in a list so len(ruleset) can be referenced later
    # each returning a boolean value cast as a float to allow for later weighting
    ruleset = [
        lambda token: float(str.isupper(token[0])), # first letter in token is capitalized
        lambda token: float(token not in english_dictionary), # token is not an english word
    ]

    # Create dummy scores object 
    # Should be 2 dimensional 
    ## dim_1 = len(array_obj) 
    ## dim_2 = len(ruleset)
    scores_obj = np.empty(
        (array_obj.shape[0],
         len(ruleset))
    )
    
    

    for t, token in enumerate(array_obj):
        for r, rule in enumerate(ruleset):
            score = rule(token)
            # apply each rule lambda in `ruleset` to each token in `array_obj`
            scores_obj[t,r] = score
            pass
    
    # Return final scores obj
    # Alternatively, mean out all the scores and return a 1-dimensional array same shape with `obj`
    return(scores_obj)

