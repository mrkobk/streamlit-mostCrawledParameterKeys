#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import pandas as pd
import csv
from urllib.parse import urlparse, parse_qs
import numpy as np



# In[4]:

def getParamKeys(url):
  parsed_url = urlparse(url)
  paramLst = parse_qs(parsed_url.query)
  keys = [k for k in paramLst.keys()]
  return keys

st.set_page_config(layout="wide")
st.title("What parameters are crawled most?")
st.sidebar.header("What's this tool about?")
st.sidebar.write('''
		Confronted with a large list of parametered URLs it can be difficult to determine
		what parameter keys are visited most.
		
		This little tool extracts the parameter keys
		from a list of URLs and provides some basic stats like
		- What unique parameter keys were present in the URL?
		- In what percentage of unique URL requests where they present	
		''')


upload = st.file_uploader("Upload List of crawled URLs", type=["csv"])
st.info("Upload a CSV file with a list of URLs and a header name of your choise in A1") 

if upload is not None:
    
    logs = pd.read_csv(upload)
    st.table(logs.head(10))
    
    logs.rename(columns={logs.columns[0]: "url_example"}, inplace=True)
    logs["param_key"] = logs["url_example"].apply(getParamKeys)
    params = logs.explode("param_key").value_counts().reset_index()
    params = params.groupby("param_key", as_index=False).agg({
    	"url_example":"first",
    	0 :"sum"
     })
    															
    params["total_param_hits"] = logs.shape[0]
    params["% of total"] = (params[0] / params["total_param_hits"]).round(4)
    params = params.rename(columns = {0:"hits"}).sort_values(by="hits",ascending=False)
    params = params[["param_key","hits","total_param_hits", "% of total", "url_example"]]
        
    st.success("Your most crawled parameters have been determined")
    st.table(params)
    
    params.to_csv("paramKey_List.csv",index=False)
    csv = params.to_csv().encode('utf-8')
    
    st.download_button(
     	label="Download table as CSV",
     	data=csv,
     	file_name='most_crawled_parameter.csv',
     	mime='text/csv')
    



