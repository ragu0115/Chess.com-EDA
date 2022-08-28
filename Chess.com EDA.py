#!/usr/bin/env python
# coding: utf-8

# # March 2022 Games of User Knightslikethis

# In[1]:


from chessdotcom import get_player_stats, get_player_game_archives, get_player_games_by_month, get_titled_players
import pprint
import requests
import pandas as pd
printer = pprint.PrettyPrinter()


# In[2]:


# Statistics of the Account knightslikethis
data = get_player_stats('knightslikethis').json
printer.pprint(data)


# ## Webscraping Online Games via Chess.com API

# In[3]:


# Get all the games played in March 2022
data1 = get_player_games_by_month('knightslikethis','2022','03').json
printer.pprint(data1)


# ## Entering Webscraped Data into a Dataframe and Preprocessing the Data

# In[4]:


# Put Games into DataFrame
df = pd.DataFrame(data1['games'])
df


# In[5]:


# DataFrame of Player with White pieces
df1 = pd.DataFrame(dict(df.white))
df1 = df1.T
df1


# In[6]:


# DataFrame of Player with Black pieces
df2 = pd.DataFrame(dict(df.black))
df2 = df2.T
df2


# In[7]:


# Dropping unecessary columns
df1 = df1.drop(columns=['@id','uuid'])


# In[8]:


# Dropping unecessary columns
df2 = df2.drop(columns=['@id','uuid'])


# In[9]:


# Columns for the White player
df1.columns = ['wht_rating', 'wht_result', 'wht_username']
df1


# In[10]:


# Columns for the Black player
df2.columns = ['blk_rating', 'blk_result', 'blk_username']
df2


# In[11]:


# Merging the 2 Dataframes
result = pd.concat([df1,df2],axis=1)
result


# In[12]:


# Results of the Game for the White Player
pd.unique(result.wht_result)


# In[13]:


# Results of the Game for the Black Player
pd.unique(result.blk_result)


# In[14]:


# Changing Game results to numbers
result=result.replace(to_replace="win",value="1")
result=result.replace(to_replace="agreed",value="0.5")
result=result.replace(to_replace="resigned",value="0")
result=result.replace(to_replace="repetition",value="0.5")
result=result.replace(to_replace="stalemate",value="0.5")
result=result.replace(to_replace="checkmated",value="0")
result=result.replace(to_replace="timeout",value="0")
result=result.replace(to_replace="timevsinsufficient",value="0.5")
result=result.replace(to_replace="insufficient",value="0.5")
result=result.replace(to_replace="abandoned",value="0")


# In[15]:


pd.set_option('display.max_rows', None)


# In[16]:


result


# In[17]:


# Dataframe of when Knightslikethis had the White pieces
white = result.loc[result['wht_username'] == "knightslikethis"]
white


# In[18]:


# Dataframe of when Knightslikethis had the White pieces
black = result.loc[result['blk_username'] == "knightslikethis"]
black


# ## Exploratory Data Analysis

# In[19]:


import matplotlib.pyplot as plt
import seaborn as sns


# ### Scatterplots

# In[20]:


# Knightslikethis with White Pieces (Key: 1 = Win, 0.5 = Draw, 0 = Loss)
ax = sns.scatterplot(x='wht_rating', y='blk_rating', data = white, hue='wht_result')
plt.title('Knightslikethis with White Pieces')
plt.show()


# In[21]:


# Knightslikethis with Black Pieces (Key: 1 = Win, 0.5 = Draw, 0 = Loss)
ax = sns.scatterplot(x='blk_rating', y='wht_rating', data = black, hue='blk_result')
plt.title('Knightslikethis with Black Pieces')
plt.show()


# ### Boxplots

# In[32]:


# Knightslikethis against White Pieces (Key: 1 = Win, 0.5 = Draw, 0 = Loss)
sns.boxplot(x='blk_result', y='wht_rating', data = black)
plt.title('Knightslikethis against White Pieces')
plt.show()


# In[31]:


# Knightslikethis against Black Pieces (Key: 1 = Win, 0.5 = Draw, 0 = Loss)
sns.boxplot(x='wht_result', y='blk_rating', data = white)
plt.title('Knightslikethis against Black Pieces')
plt.show()


# ### Pie Charts

# In[42]:


# White Piece Game Results (Key: 1 = Win, 0.5 = Draw, 0 = Loss)
white.groupby('wht_result').size().plot(kind='pie', autopct='%.2f')
plt.title('White Piece Game Results')
plt.show()


# In[43]:


# Black Piece Game Results (Key: 1 = Win, 0.5 = Draw, 0 = Loss)
black.groupby('blk_result').size().plot(kind='pie', autopct='%.2f')
plt.title('Black Piece Game Results')
plt.show()

