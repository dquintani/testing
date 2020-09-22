#!/usr/bin/env python
# coding: utf-8

# # COVID-19 Testing en Bolivia, serie de tiempo (confirmados + descartados)

# In[1]:


print('works')


# In[2]:


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import io

import matplotlib.dates as dates

import csv

import unicodedata

print('imports successfull')


# # CONFIRMADOS (@mauforonda)

# In[3]:


#RAW
url = "https://raw.githubusercontent.com/mauforonda/covid19-bolivia/master/confirmados.csv"
download = requests.get(url).content
confirmados = pd.read_csv(io.StringIO(download.decode('utf-8')))
confirmados.head()


# In[4]:
print('43')

#change to datetime - confirmados
confirmados['Fecha'] = pd.to_datetime(confirmados['Fecha'])
confirmados.head()


# In[5]:


#set index confirmados
confirmados = confirmados.set_index('Fecha')
confirmados.head()


# In[6]:


#change to lowercase
confirmados.columns = confirmados.columns.str.lower()
confirmados.head()


# In[7]:


#confirmados.potosí.rename({'potosí':'potosi'}, inplace=True)


# In[8]:
print('73')


confirmados = confirmados.rename(columns = {'potosí':'potosi'})
# confirmados['potosí'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
# confirmados.head()

# confirmados.potosí = confirmados.potosí.str.replace('potosí', 'potosi')
# confirmados.head()

# confirmados.potosí = confirmados.potosí.rename({'potosí':'potosi'}, inplace=True, axis=1)
# confirmados.potosi()

#data.rename(columns={'gdp':'log(gdp)'}, inplace=True)
#df.columns = df.columns.str.replace('gdp', 'log(gdp)')
#df=df.rename(columns = {'two':'new_name'})


# In[9]:


#plot
plt.plot(confirmados)
plt.legend(confirmados)
plt.show()


# # DESCARTADOS (@edu_arraya, pr0nstar)

# In[10]:
print('103')


#RAW
url= "https://raw.githubusercontent.com/pr0nstar/covid19-pruebas/master/data/testing.csv"
download = requests.get(url).content
testing = pd.read_csv(io.StringIO(download.decode('utf-8')))

testing.head()


# In[11]:


#MultIndex Sospechosos and Descartados
testing_columns = [idx.lower() for idx in testing.columns[1:] if 'Unnamed' not in idx]
testing_idx = pd.MultiIndex.from_product([testing_columns, testing.iloc[0].reset_index()[1:][0].unique()])


testing.head()


# In[12]:


#Index Dates
testing['Fecha'] = pd.to_datetime(testing['Fecha'])
testing = testing.set_index('Fecha')


testing.head()


# In[13]:


testing = testing.iloc[1:]

testing.head()

print('143')

# In[14]:


#?????
testing = testing.iloc[1:]
testing.columns = testing_idx

testing.head()


# In[15]:


#re-organize table

testing = testing.astype(np.float32)
testing = testing.interpolate(method='quadratic')
testing = testing.swaplevel(axis=1).sort_index(level=0, axis=1)

testing.head()


# In[16]:


# #delete sospechosos columns method 2
# testing.Sospechosos.drop(testing.Sospechosos, axis=1)
# testing.Sospechosos.head()
print('173')


# In[17]:


# testing.drop(columns= ['beni','tarija', 'chuquisaca', 'cochabamba', 'la paz', 'oruro', 'pando', 'potosi', 'santa cruz'])
# testing.head()


# In[18]:


testing.Descartados.head()


# In[19]:


type(testing)


# In[20]:


plt.plot(testing.Descartados)
plt.legend()
#plt.show(testing)


# In[21]:


# tot_tests = ([confirmados] + [testing.Descartados])
# tot_tests


# In[22]:


#type(tot_tests)


# In[23]:


# df = pd.DataFrame(tot_tests)
# df.to_csv('file2.csv', index=False, header=False,)
# df

print('223')

# In[24]:


tot_tests = (confirmados + testing.Descartados)


# In[25]:

print('233')

tot_tests


# In[26]:

os.remove("./tot_tests.csv")

tot_tests.to_csv("./tot_tests.csv", sep=',',index=True)


# In[233]:


#np.savetxt("tot_tests.csv", tot_tests, delimiter=",", fmt='%s')

print('finished!')

