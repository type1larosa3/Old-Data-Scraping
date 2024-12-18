# %%
import numpy as np, requests, pandas as pd, re
from bs4 import BeautifulSoup

r = requests.get("https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-12-20")
soup = BeautifulSoup(r.text, "html.parser")
soup.prettify()

# %%
soup.find_all('div', 'sorted-by-overview-container sortedContainer')

# %%
soup.find_all('div', 'sorted-by-sideboard-container clearfix element')

# %%
maindeck_data_temp = soup.find_all('div', 'sorted-by-overview-container sortedContainer')

# %%
sideboard_data_temp = soup.find_all('div', 'sorted-by-sideboard-container clearfix element')

# %%
#sideboard div in overview is separate from main deck div. 
#does help keep track of placings.

hashmap = dict()

maindeck_data = []
for deck in maindeck_data_temp:
    maindeck_data.append(str(deck))

sideboard_data = []
for s in sideboard_data_temp:
    sideboard_data.append(str(s))
    
for i in range(0, 32):
    current_deck = maindeck_data[i]
    maindeck_soup = BeautifulSoup(current_deck, "html.parser")
    maindeck_card_info = maindeck_soup.find_all('span', 'row')
    
    in_main = False
    
    for card in maindeck_card_info:
        n_match = re.search('<span class="card-count">(\d+)</span>', str(card))
        num = int(n_match.group(1))
        name_match = re.search('<span class="card-name">(.+)', str(card))
        string_data = str(name_match.group(1))
        name = ''
        
        if string_data[0] == '<':
            loc = string_data.find('>')
            start = loc + 1
            end = 0
            for j in range(start, len(string_data)):
                if string_data[j] == '<':
                    end = j
                    break;
        
            name = string_data[start:end]
        else:
            end = 0
            for j in range(0, len(string_data)):
                if string_data[j] == '<':
                    end = j
            
            name = string_data[0:end]
        
        if name in hashmap.keys():
            card_hash = hashmap[name]
            card_hash['Top 32 Count Main'] = card_hash['Top 32 Count Main'] + 1
            
            if i <= 7:
                card_hash['Top 8 Count Main'] = card_hash['Top 8 Count Main'] + 1
            
            if num == 1:
                card_hash['Main 1'] = card_hash['Main 1'] + 1
            elif num == 2:
                card_hash['Main 2'] = card_hash['Main 2'] + 1
            elif num == 3:
                card_hash['Main 3'] = card_hash['Main 3'] + 1
            elif num == 4:
                card_hash['Main 4'] = card_hash['Main 4'] + 1
        
            hashmap[name] = card_hash
        else:
            if num <= 4:
                card_hash = dict()
                card_hash['Top 32 Count Main'] = 1
                card_hash['Top 8 Count Main'] = 0
                if i <= 7:
                    card_hash['Top 8 Count Main'] = 1
            
                if num == 1:
                    card_hash['Main 1'] = 1
                    card_hash['Main 2'] = 0
                    card_hash['Main 3'] = 0
                    card_hash['Main 4'] = 0
                elif num == 2:
                    card_hash['Main 1'] = 0
                    card_hash['Main 2'] = 1
                    card_hash['Main 3'] = 0
                    card_hash['Main 4'] = 0
                elif num == 3:
                    card_hash['Main 1'] = 0
                    card_hash['Main 2'] = 0
                    card_hash['Main 3'] = 1
                    card_hash['Main 4'] = 0
                elif num == 4:
                    card_hash['Main 1'] = 0
                    card_hash['Main 2'] = 0
                    card_hash['Main 3'] = 0
                    card_hash['Main 4'] = 1
                    
                card_hash['Side 1'] = 0
                card_hash['Side 2'] = 0
                card_hash['Side 3'] = 0
                card_hash['Side 4'] = 0
                card_hash['Top 8 Count Side'] = 0
                card_hash['Top 32 Count Side'] = 0
            
            hashmap[name] = card_hash
                
    current_deck = sideboard_data[i]
    sideboard_soup = BeautifulSoup(current_deck, "html.parser")
    sideboard_card_info = sideboard_soup.find_all('span', 'row')
    
    
    for card in sideboard_card_info:
        n_match = re.search('<span class="card-count">(\d+)</span>', str(card))
        num = int(n_match.group(1))
        name_match = re.search('<span class="card-name">(.+)', str(card))
        string_data = str(name_match.group(1))
        name = ''
        
        if string_data[0] == '<':
            loc = string_data.find('>')
            start = loc + 1
            end = 0
            for j in range(start, len(string_data)):
                if string_data[j] == '<':
                    end = j
                    break;
        
            name = string_data[start:end]
        else:
            end = 0
            for j in range(0, len(string_data)):
                if string_data[j] == '<':
                    end = j
            
            name = string_data[0:end]
            
        if name in hashmap.keys():
            card_hash = hashmap[name]
            card_hash['Top 32 Count Side'] = card_hash['Top 32 Count Side'] + 1
            
            if i <= 7:
                card_hash['Top 8 Count Side'] = card_hash['Top 8 Count Side'] + 1
            
            if num == 1:
                card_hash['Side 1'] = card_hash['Side 1'] + 1
            elif num == 2:
                card_hash['Side 2'] = card_hash['Side 2'] + 1
            elif num == 3:
                card_hash['Side 3'] = card_hash['Side 3'] + 1
            elif num == 4:
                card_hash['Side 4'] = card_hash['Side 4'] + 1
        
            hashmap[name] = card_hash
        else:
            if num <= 4:
                card_hash = dict()
                card_hash['Top 32 Count Side'] = 1
                card_hash['Top 8 Count Side'] = 0
                if i <= 7:
                    card_hash['Top 8 Count Side'] = 1
            
                if num == 1:
                    card_hash['Side 1'] = 1
                    card_hash['Side 2'] = 0
                    card_hash['Side 3'] = 0
                    card_hash['Side 4'] = 0
                elif num == 2:
                    card_hash['Side 1'] = 0
                    card_hash['Side 2'] = 1
                    card_hash['Side 3'] = 0
                    card_hash['Side 4'] = 0
                elif num == 3:
                    card_hash['Side 1'] = 0
                    card_hash['Side 2'] = 0
                    card_hash['Side 3'] = 1
                    card_hash['Side 4'] = 0
                elif num == 4:
                    card_hash['Side 1'] = 0
                    card_hash['Side 2'] = 0
                    card_hash['Side 3'] = 0
                    card_hash['Side 4'] = 1
                    
                card_hash['Main 1'] = 0
                card_hash['Main 2'] = 0
                card_hash['Main 3'] = 0
                card_hash['Main 4'] = 0
                card_hash['Top 8 Count Main'] = 0
                card_hash['Top 32 Count Main'] = 0
            
            hashmap[name] = card_hash




# %%


# %%
challenge_links = ["https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-06-06",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-06-07",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-06-13",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-06-14",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-06-20",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-06-21",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-06-27",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-06-28",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-07-05",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-07-11",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-07-12",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-07-18",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-07-19",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-07-25",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-07-26",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-08-02",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-08-08",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-08-09",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-08-15",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-08-16",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-08-22",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-08-23",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-08-29",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-08-30",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-09-05",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-09-06",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-09-12",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-09-13",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-09-19",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-09-20",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-09-27",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-10-03",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-10-04",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-10-10",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-10-11",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-10-17",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-10-18",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-10-24",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-10-25",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-10-31",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-11-01",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-11-07",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-11-08",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-11-15",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-11-21",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-11-22",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-11-28",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-11-29",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-12-05",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-12-06",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-12-13",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-12-19",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-12-20",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-12-26",
                   "https://magic.wizards.com/en/articles/archive/mtgo-standings/modern-challenge-2021-12-27"
                  ]

# %%
hashmap = dict()
for link in challenge_links:
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "html.parser")
    
    maindeck_data_temp = soup.find_all('div', 'sorted-by-overview-container sortedContainer')
    sideboard_data_temp = soup.find_all('div', 'sorted-by-sideboard-container clearfix element')
    
    maindeck_data = []
    for deck in maindeck_data_temp:
        maindeck_data.append(str(deck))

    sideboard_data = []
    for s in sideboard_data_temp:
        sideboard_data.append(str(s))
    
    for i in range(0, 32):
        current_deck = maindeck_data[i]
        maindeck_soup = BeautifulSoup(current_deck, "html.parser")
        maindeck_card_info = maindeck_soup.find_all('span', 'row')
    
        for card in maindeck_card_info:
            n_match = re.search('<span class="card-count">(\d+)</span>', str(card))
            num = int(n_match.group(1))
            name_match = re.search('<span class="card-name">(.+)', str(card))
            string_data = str(name_match.group(1))
            name = ''
        
            if string_data[0] == '<':
                loc = string_data.find('>')
                start = loc + 1
                end = 0
                for j in range(start, len(string_data)):
                    if string_data[j] == '<':
                        end = j
                        break;
        
                name = string_data[start:end]
            else:
                end = 0
                for j in range(0, len(string_data)):
                    if string_data[j] == '<':
                        end = j
            
                name = string_data[0:end]
        
            if name in hashmap.keys():
                card_hash = hashmap[name]
                card_hash['Top 32 Count Main'] = card_hash['Top 32 Count Main'] + 1
            
                if i <= 7:
                    card_hash['Top 8 Count Main'] = card_hash['Top 8 Count Main'] + 1
            
                if num == 1:
                    card_hash['Main 1'] = card_hash['Main 1'] + 1
                elif num == 2:
                    card_hash['Main 2'] = card_hash['Main 2'] + 1
                elif num == 3:
                    card_hash['Main 3'] = card_hash['Main 3'] + 1
                elif num == 4:
                    card_hash['Main 4'] = card_hash['Main 4'] + 1
        
                hashmap[name] = card_hash
            else:
                if num <= 4:
                    card_hash = dict()
                    card_hash['Top 32 Count Main'] = 1
                    card_hash['Top 8 Count Main'] = 0
                    if i <= 7:
                        card_hash['Top 8 Count Main'] = 1
            
                    if num == 1:
                        card_hash['Main 1'] = 1
                        card_hash['Main 2'] = 0
                        card_hash['Main 3'] = 0
                        card_hash['Main 4'] = 0
                    elif num == 2:
                        card_hash['Main 1'] = 0
                        card_hash['Main 2'] = 1
                        card_hash['Main 3'] = 0
                        card_hash['Main 4'] = 0
                    elif num == 3:
                        card_hash['Main 1'] = 0
                        card_hash['Main 2'] = 0
                        card_hash['Main 3'] = 1
                        card_hash['Main 4'] = 0
                    elif num == 4:
                        card_hash['Main 1'] = 0
                        card_hash['Main 2'] = 0
                        card_hash['Main 3'] = 0
                        card_hash['Main 4'] = 1
                    
                    card_hash['Side 1'] = 0
                    card_hash['Side 2'] = 0
                    card_hash['Side 3'] = 0
                    card_hash['Side 4'] = 0
                    card_hash['Top 8 Count Side'] = 0
                    card_hash['Top 32 Count Side'] = 0
            
                hashmap[name] = card_hash
                
        current_deck = sideboard_data[i]
        sideboard_soup = BeautifulSoup(current_deck, "html.parser")
        sideboard_card_info = sideboard_soup.find_all('span', 'row')
    
    
        for card in sideboard_card_info:
            n_match = re.search('<span class="card-count">(\d+)</span>', str(card))
            num = int(n_match.group(1))
            name_match = re.search('<span class="card-name">(.+)', str(card))
            string_data = str(name_match.group(1))
            name = ''
        
            if string_data[0] == '<':
                loc = string_data.find('>')
                start = loc + 1
                end = 0
                for j in range(start, len(string_data)):
                    if string_data[j] == '<':
                        end = j
                        break;
        
                name = string_data[start:end]
            else:
                end = 0
                for j in range(0, len(string_data)):
                    if string_data[j] == '<':
                        end = j
            
                name = string_data[0:end]
            
            if name in hashmap.keys():
                card_hash = hashmap[name]
                card_hash['Top 32 Count Side'] = card_hash['Top 32 Count Side'] + 1
            
                if i <= 7:
                    card_hash['Top 8 Count Side'] = card_hash['Top 8 Count Side'] + 1
            
                if num == 1:
                    card_hash['Side 1'] = card_hash['Side 1'] + 1
                elif num == 2:
                    card_hash['Side 2'] = card_hash['Side 2'] + 1
                elif num == 3:
                    card_hash['Side 3'] = card_hash['Side 3'] + 1
                elif num == 4:
                    card_hash['Side 4'] = card_hash['Side 4'] + 1
        
                hashmap[name] = card_hash
            else:
                if num <= 4:
                    card_hash = dict()
                    card_hash['Top 32 Count Side'] = 1
                    card_hash['Top 8 Count Side'] = 0
                    if i <= 7:
                        card_hash['Top 8 Count Side'] = 1
            
                    if num == 1:
                        card_hash['Side 1'] = 1
                        card_hash['Side 2'] = 0
                        card_hash['Side 3'] = 0
                        card_hash['Side 4'] = 0
                    elif num == 2:
                        card_hash['Side 1'] = 0
                        card_hash['Side 2'] = 1
                        card_hash['Side 3'] = 0
                        card_hash['Side 4'] = 0
                    elif num == 3:
                        card_hash['Side 1'] = 0
                        card_hash['Side 2'] = 0
                        card_hash['Side 3'] = 1
                        card_hash['Side 4'] = 0
                    elif num == 4:
                        card_hash['Side 1'] = 0
                        card_hash['Side 2'] = 0
                        card_hash['Side 3'] = 0
                        card_hash['Side 4'] = 1
                    
                    card_hash['Main 1'] = 0
                    card_hash['Main 2'] = 0
                    card_hash['Main 3'] = 0
                    card_hash['Main 4'] = 0
                    card_hash['Top 8 Count Main'] = 0
                    card_hash['Top 32 Count Main'] = 0
            
                hashmap[name] = card_hash
                

hashmap

# %%
df_data = []
for card in hashmap.keys():
    row = []
    card_hash = hashmap[card]
    row.append(card)
    row.append(card_hash['Top 8 Count Main'])
    row.append(card_hash['Top 32 Count Main'])
    row.append(card_hash['Main 1'])
    row.append(card_hash['Main 2'])
    row.append(card_hash['Main 3'])
    row.append(card_hash['Main 4'])
    row.append(card_hash['Top 8 Count Side'])
    row.append(card_hash['Top 32 Count Side'])
    row.append(card_hash['Side 1'])
    row.append(card_hash['Side 2'])
    row.append(card_hash['Side 3'])
    row.append(card_hash['Side 4'])
    df_data.append(row)
    
df = pd.DataFrame(df_data, 
                  columns = ['Card Name', 'Top 8 Count Main', 'Top 32 Count Main', 'Main 1', 
                             'Main 2', 'Main 3', 'Main 4', 'Top 8 Count Side', 'Top 32 Count Side', 
                             'Side 1', 'Side 2', 'Side 3', 'Side 4'])
df = df.set_index('Card Name')

# %%
pd.set_option('display.max_rows', None)
df.sort_values(by = ['Top 8 Count Main'], ascending = False)

# %%
len(challenge_links)

# %%
55*32

# %%
8*55

# %%
117/440

# %%



