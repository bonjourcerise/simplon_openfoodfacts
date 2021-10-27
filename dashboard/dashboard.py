#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image


df_nutriscore = pd.read_csv(r"C:\Users\veron\Desktop\Deploiement\dashboard\data\data.csv")
st.set_option('deprecation.showPyplotGlobalUse', False)

image = Image.open(r"C:\Users\veron\Desktop\Deploiement\dashboard\img\orange.jpg")
st.image(image)

st.title("Analyse des jus d'orange en France")

# visualisation 1
fig1 = px.bar(df_nutriscore, x="nutriscore_grade", color="nutriscore_grade",
              labels={"nutriscore_grade": "Nutriscore","count": "Nombre de produits"},
              title="Répartition des jus d'orange par Nutriscore",
              category_orders={"nutriscore_grade":['a','b','c','d','e']})
st.plotly_chart(fig1)

# visualisation 3

# new df for sugars
df_sugars = df_nutriscore

# delete product with sugars_100g = 0
df_sugars = df_sugars[df_sugars.sugars_100g != 0]

# create 7 bins starting with 0 up to 50
bins = np.arange(0, 30, 5)

# use pd.cut to create the bins
df_nutriscore['sugars_100g'] = pd.cut(df_nutriscore['sugars_100g'], bins, include_lowest=True)

# count the values in each bin. Bins are sorted based on the occurance (from most populated to the least one)
agg = df_nutriscore['sugars_100g'].value_counts()

# sort the values according to the bins (`sort_index`), turn into data frame (`to_frame`) and reset index
agg = agg.sort_index().to_frame().reset_index()

# rename index (containing the bin range to bins)
agg.rename(columns={"index":"bins"}, inplace=True)

# Plotly cannot work with categories index, so we need to turn it into string
agg["bins"] = agg["bins"].astype("str")

#pie chart
fig3 = px.pie(agg, values='sugars_100g', names='bins', title="Répartition des produits avec taux de sucre entre 0,0001 et 50 grammes")
st.plotly_chart(fig3)

