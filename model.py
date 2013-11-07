import pandas as pd
import numpy as np
import time
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier

def time(dataframe):
	time = ['registered','recent_date1','recent_date2','recent_date3','recent_date4','recent_date5']
	for col in time:
	    new_series = []
	    hours = []
	    for item in dataframe[col]:
	        if pd.isnull(item):
	            new_series.append(item)
	            continue
	        new_series.append(datetime.fromtimestamp(item))
	    dataframe[col] = new_series
	    if col == 'registered':
	    	hours = []
	    	for item in new_series:
	    		if pd.isnull(item):
	    			hours.append(item)
	    		hours.append(item.strftime(%H))
	    	dataframe['hour_registered'] = hours
	return dataframe


	dataframe['hour_registered'] = map(strftime('H'dataframe['registered']
	return 