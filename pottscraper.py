from mechanize import Browser
from bs4 import *
from time import *
import re
import datetime

mech = Browser()

mech.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

mech.set_handle_robots(False)

today = str(datetime.date.today().strftime("%m-%d-%Y"))

f = open('pott-as-of-' + today + '.txt','wb')

baseurl = "http://pottcountysheriff.com/public-awareness/incarcerations.php"

counter = 0
while counter < 5:
    try:
        page = mech.open(baseurl)
        counter = 6
    except:
        print "The page didn't open on try No. " + str(counter+1) +". Feel bad."
        counter += 1
        sleep(30)

html = page.read()
print "Reading page."

# un-comment table cells
clean_html = html.replace("<!--","").replace("-->","")

soup = BeautifulSoup(clean_html, "html5lib")
print "Souping page."

table = soup.find('table', {'width': '90%'})

for row in table.findAll('tr')[1:]:
    col = row.findAll('td')
    
    try:
        rawname = col[0].get_text(strip=True).upper()
        last = rawname.split(', ')[0]
        first = rawname.split(', ')[1]
    except:
        last = "MCGURT"
        first = "TURD"
   
    print first, last
    
    try:
        date_conf = col[1].get_text(strip=True)
    except:
        date_conf = "Not reported"
    
    try:
        time_conf = col[2].get_text(strip=True)
    except:
        time_conf = "Not reported"
    
    try:
        age = col[3].get_text(strip=True)
    except:
        age = "Not reported"
    
    try:
        height = col[4].get_text(strip=True)
    except:
        height = "Not reported"
    
    try:
        weight = col[5].get_text(strip=True)
    except:
        weight = "Not reported"
    
    try:
        sex = col[6].get_text(strip=True)
    except:
        sex = "Not reported"
        
    try:
        race = col[7].get_text(strip=True)
    except:
        race = "Not reported"
    
    # pipe delimiters for multiple crimes
    try:
        for e in col[8].findAll('br'):
            e.replace_with(" | ")
        charges = col[8].get_text(strip=True).rstrip('|')
    except:
        charges = "Not reported"
        
    # and for multiple bond amounts
    try:
        for e in col[9].findAll('br'):
            e.replace_with(" | ")
        bond = col[9].get_text(strip=True).rstrip('|')
    except:
        bond = "Not reported"
        
    fullrec = (last, first, date_conf, time_conf, age, height, weight, sex, race, charges, bond, '\n')
    f.write("\t".join(fullrec))
    sleep(1)
f.flush()
f.close()