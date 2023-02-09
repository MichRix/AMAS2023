#%%
import cloudscraper
from bs4 import BeautifulSoup

# %%
scraper = cloudscraper.create_scraper()
response14 = scraper.get("https://kenpom.com/index.php?y=2014")
soup = BeautifulSoup(response14.content, features="html.parser")
print(soup)
# %%
headers = soup.find(class_ = 'thead2')
headers2 = headers.find_all('th')

header_list = []
for i in headers2:
    text = i.get_text()
    header_list.append(text)
header_list.remove('AdjEM')

print(header_list)
# %%
body = soup.find('tbody')
body2 = body.find_all('td')

body_list = []
for i in body2:
    text = i.get_text()
    #body_list.append(text)
    print(text)
# %%
