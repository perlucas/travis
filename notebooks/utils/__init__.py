import pandas as pd

from .bot_tracker import *
from .bot import *
from .long_position import *

def load_dataset(name, index_name='Date'):
    '''
    Load the contents of the given CSV stock prices file into a brand new pandas dataset
    '''
    df = pd.read_csv(name, parse_dates=True, index_col=index_name)
    return df
