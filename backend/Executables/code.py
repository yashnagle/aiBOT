import sys
import pandas as pd
import os

#Supports only 1 dataframe right now

def import_df(file_name):
    dir = '/Users/yash/Documents/Personal/aiBot/ai-bot/backend/'

    file_name = str(file_name[0]) #update this to make it accept more, also add a for loop for the same

    try:
        df = pd.read_csv(dir+str(file_name))
    except Exception as e:
        return {'Status':f'import failed! {e}'}
    
    else:
        return {'Status':'import successful!'}



    return 'hi'