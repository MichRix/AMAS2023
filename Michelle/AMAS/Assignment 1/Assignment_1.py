#%%
import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %%

def get_headers(soup): # Function that gets relevant headers
    headers = []
    results = soup.find(class_='thead2')
    ranks = results.find_all('th')
    for rank in ranks:
        text = rank.get_text()
        headers.append(text)
    headers.remove('AdjEM')
    return headers

def get_data(soup): # Function that gets the relevant data
	results = soup.find("tbody")
	list_of_list = []
	classes_body = ['hard_left', 'next_left', 'conf', 'wl', 'td-left']
	for cl in classes_body:
		list_ranks = []
		ranks = results.find_all("td", class_=cl)
		if cl == 'td-left':
			for rank in ranks:
				text = rank.get_text()
				list_ranks.append(text)
			for i in range(8):
				list_list = [float(i) for i in list_ranks[i::8]]
				list_of_list.append(list_list)
		else:
			for rank in ranks:
				text = rank.get_text()
				list_ranks.append(text)
			list_of_list.append(list_ranks)
	return list_of_list

def create_df(headers, data): # Combine headers 
    dictionary = dict(zip(headers, data))
    df = pd.DataFrame(dictionary)
    df['Team'] = df['Team'].str.replace('\d+', '')
    return df




#%%
scraper = cloudscraper.create_scraper()

# DATA FROM 2014
response14 = scraper.get("https://kenpom.com/index.php?y=2014")
soup = BeautifulSoup(response14.content, features="html.parser")  #soup 2012
df_2014 = create_df(get_headers(soup),get_data(soup))

# DATA FROM 2009
response9 = scraper.get("https://kenpom.com/index.php?y=2014")
soup9 = BeautifulSoup(response9.content, features="html.parser")  #soup 2012
df_2009 = create_df(get_headers(soup9),get_data(soup9))

# %%
'''
headers = soup.find(class_ = 'thead2')
headers2 = headers.find_all('th')

header_list = []
for i in headers2:
    text = i.get_text()
    header_list.append(text)
header_list.remove('AdjEM')

print(header_list)
'''
# %%
'''
body = soup.find('tbody')
body2 = body.find_all('td')

body_list = []
for i in body2:
    text = i.get_text()
    if i != 6:
        body_list.append(text)
    print(text)
    '''

# %%
# fig, ax = plt.subplots(figsize=(7, 9))
print(df_2014['Conf'])
# %%

def sort_as_dict(df, header):
	dictionary = {}
	for i,key in enumerate(df[header]):
		if not key in dictionary:
			dictionary[key] = []
		if key in dictionary:
			dictionary[key].append(i)
	return dictionary

#%%
conference_2014 = sort_as_dict(df_2014, 'Conf')
conference_2009 = sort_as_dict(df_2009, 'Conf')

conferences = ['ACC', 'SEC', 'B10', 'BSky', 'A10']

# %%
fig, ax = plt.subplots(figsize=(10,10))
alphas = [1,0.9,0.8,0.7,0.6,0.5]
for conf_key, a in zip(conferences, alphas):
    ax.hist(df_2014['AdjD'][conference_2014[conf_key]], bins=10, label=f'{conf_key}', alpha=a, linewidth=10)
ax.legend(title='Conference')
ax.set_xlabel('Adjusted Defense Score')
ax.set_ylabel('Counts')
ax.set_title('Adjusted defense for college basketball teams in terms of conference');
# %%
# EXERCISE 1

conferences = ['ACC', 'SEC', 'B10', 'BSky', 'A10']


ACC_arr = df_2014['AdjD'][conference_2014['ACC']]
SEC_arr = df_2014['AdjD'][conference_2014['SEC']]
B10_arr = df_2014['AdjD'][conference_2014['B10']]
BSky_arr = df_2014['AdjD'][conference_2014['BSky']]
A10_arr = df_2014['AdjD'][conference_2014['A10']]


#%%
data_min = min(min(ACC_arr), min(SEC_arr), min(B10_arr), min(BSky_arr), min(A10_arr))
data_max = max(max(ACC_arr), max(SEC_arr), max(B10_arr), max(BSky_arr), max(A10_arr))

# Defining the bin width and the number og bins to use.
bin_width = 4.0
n_bins = len(np.arange(data_min, data_max, bin_width))

# Defining the position of the ticks on the x axis. 
tick_position = np.array([0, bin_width, 2*bin_width, 3*bin_width, 4*bin_width, 5*bin_width, 6*bin_width])
tick_position += (data_min + bin_width/2)
tick_name = [f'[{data_min + i*bin_width},{data_min + (i+1) * bin_width})' for i in range(n_bins+1)]

fig, ax = plt.subplots(figsize = (11,6))
ax.hist([ACC_arr, SEC_arr, B10_arr, BSky_arr, A10_arr], bins = n_bins, label = conferences)
ax.set_xticks(tick_position)
ax.set_xticklabels(tick_name, fontsize = 11)
ax.set_title('Adjusted defense of 5 different conferences', fontsize=15)
ax.set_ylabel('Count', fontsize=13)
ax.set_xlabel('Adjusted defense',fontsize=13)
ax.legend(fontsize=12);

# %%
print(tick_position)
# %%
print(np.arange(data_min, data_max, 5))
# %%
print(n_bins)
# %%
data_max
# %%
bin_width
# %%
np.arange(data_min, data_max, 4)
# %%
print(A10_arr)
# %%
