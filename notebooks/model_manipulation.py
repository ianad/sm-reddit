import praw

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