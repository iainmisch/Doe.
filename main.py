# Read the <h3> tags to find the branch from which the bill was introduced
def findBranch(soup):
  h3_soup = soup.find_all('h3')
  for i in h3_soup:
    if i.string.find('SB') >= 0:
      return 'SB'
    elif i.string.find('SJ') >= 0:
      return 'SJ'
    elif i.string.find('SR') >= 0:
      return 'SR'
    elif i.string.find('HB') >= 0:
      return 'HB'
    elif i.string.find('HJ') >= 0:
      return 'HJ'
    elif i.string.find('HR') >= 0:
      return 'HR'
    return 'Error: No Branch Found'  
# Read the <h3> branch, split along whitespaces, extract the number 
def findNumber(soup):
  h3_soup = soup.find_all('h3')
  for i in h3_soup:
    splitted = i.string.split()
    for idx in splitted:
      if idx.isdigit():
        return idx

# Read the <b> tags, find the one that ends at a period
def findDef(soup):
  p_soup = soup.find_all('p')
  p_sentence = [p.text for p in p_soup]
  if p_sentence is not None:
    for i in p_sentence:
      period_count = 0
      end = len(i)
      for j in range(len(i)):
        if i[j] == '.':
          period_count += 1
          if period_count == 2:
            end = j
            break
    substring = i[:end + 1]
    return substring

      
      #if ';' in text:
       # next_sibling = i.find_next_sibling()
        #period_index = next_sibling.find('.')
        #substring = next_sibling[:period_index]
        #result.append(substring)
  #return result
      #if i is not None and ';' in i.string:            
        #substring = i.find_next_sibling().string
      #substring = i.find_next_sibling()[:period_index]
        #result.append(substring)


# First determine which branch it is, then generate a keyword phrase to determine if it is passed or pending
# Ignore anything that is failed
def findStatus(soup):

  # Generic fail keywords for every branch
  keyword_fail = [': Left in', 'Failed to', 'stricken', 'Incorporated', 'Tabled in', ': Passed by indefinitely']
  
  if (findBranch(soup) == 'HJ'):
    keyword_pass = ['as passed', 'Agreed to by House', 'Agreed to by Senate']
  elif (findBranch(soup) == 'HR'):
    keyword_pass = ['as passed', 'Agreed to by House']
  elif (findBranch(soup) == 'HB'):
    keyword_pass = ['Governor: Approved']
  elif (findBranch(soup) == 'SB'):
    keyword_pass = ['Governor: Approved']
  elif (findBranch(soup) == 'SJ'):
    keyword_pass = ['as passed', 'Agreed to by House', 'Agreed to by Senate']
  elif (findBranch(soup) == 'SR'):
    keyword_pass = ['as passed', 'Agreed to by Senate']
  else:
    return 'Pending'

    
  # Try to find the dates to see if pending bills have failed
  li_soup = soup.find_all('li')
  li_words = [li.text for li in li_soup]
  for idx in li_words:
    splitted = idx.split()
    for i in splitted:
      # If a format for a date is found, store that date
      if (i.find('/') >= 0 and any(char.isdigit() for char in i)):
        date = datetime.strptime(i, '%m/%d/%y')

        
    # Go through every possibility of pass phrases, if match then bill is passed
  for passed in keyword_pass:
    if (idx.find(passed) >= 0):
      return 'Passed'
    # Go through every possibility of fail phrases, if match then bill has failed
  for failed in keyword_fail:
    if (idx.find(failed) >= 0):
        # If gap between 
      if (idx.find(': Passed by indefinitely') >= 0 and datetime.now().date() - date < 90):
        return 'Pending'
      else:
        return 'Failed'

  return 'Pending'

# Use structure of status to find date introduced and last date of amendment   
def findDate(soup):
  li_soup = soup.find_all('li')
  li_words = [li.text for li in li_soup]
  first = True
  for idx in li_words:
    splitted = idx.split()
    for i in splitted:
      # If a format for a date is found, store that date
      if (i.find('/') >= 0 and any(char.isdigit() for char in i)):
        if (first):
          first_date = datetime.strptime(i, '%m/%d/%y')
          first = False
        date = datetime.strptime(i, '%m/%d/%y')
  return [first_date, date]

# Beginning of Main Code
import requests
from bs4 import BeautifulSoup
from datetime import datetime

while(True):
  # Pull the URL and load up the webpage
  #URL = "https://lis.virginia.gov/cgi-bin/legp604.exe?231+sum+HB1395"
  URL = "https://lis.virginia.gov/cgi-bin/legp604.exe?ses=231&typ=bil&val=hb2278"
  page = requests.get(URL) 

  # Allows the user to ask for a bill number
  response = input("Please input a bill number to get relevant information (with no spaces): ")

  # Use the search bar to search the requested bill
  try:
    query = requests.get("https://lis.virginia.gov/cgi-bin/legp604.exe?ses=231&typ=bil&val=" + response.lower())
    search_soup = BeautifulSoup(query.content, "html.parser")

    print('\n\n\n\n' + findBranch(search_soup) + ' ' + findNumber(search_soup)+'\n-------------------------------')
    print(findDef(search_soup).ljust(40, ' '))
    print('-------------------------------\n'+'Status: ' + findStatus(search_soup))
    print('-------------------------------\nDate:')
    print('Most recently changed: ')
    print(findDate(search_soup)[1])
    print('Introduced: ')
    print(findDate(search_soup)[0])
  
  except:
    print("Invalid bill: Doesn't Exist")
    break
    
  # Save the HTML Code with all of the tags
  #soup = BeautifulSoup(page.content, "html.parser")

  


