#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import pandas as pd
import csv



# In[4]:

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
    
    file_details = {
        "filename":upload.name,
        "filetype":upload.type,
        "filesize":upload.size
                   }
    logs = pd.read_csv(upload)
    st.table(logs.head(10))
    
    logs = logs[logs.iloc[:,0].str.contains('\?',regex=True)]
    logs_p = logs.replace(".+\?","",regex=True)
    logs_p = pd.DataFrame(logs_p.iloc[:,0].str.split('&').tolist())
    logs_p = logs_p.replace("\=.+","",regex=True)

    paramLst = pd.melt(logs_p).iloc[:,1]
    paramLst = paramLst.value_counts().reset_index()
    paramLst.dropna()

    paramLst["total"] = logs_p.shape[0]
    paramLst["%"] = (paramLst["value"] / paramLst["total"]).round(4)
    paramLst = paramLst.rename(columns = {
        "index":"param_key",
        "value":"hits",
        "total":"total_param_hits",
        "%":"% of total"
        })

    st.success("Your most crawled parameters have been determined")
    st.table(paramLst)
    
    csv = paramLst.to_csv().encode('utf-8')
    
    st.download_button(
     	label="Download table as CSV",
     	data=csv,
     	file_name='most_crawled_parameter.csv',
     	mime='text/csv')
    



