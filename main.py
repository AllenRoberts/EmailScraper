import re
import requests
from bs4 import BeautifulSoup
from time import time as timer

__author__ = "Allen Roberts"
__credits__ = ["Allen Roberts"]
__version__ = "1.0.0"
__maintainer__ = "Allen Roberts"


def readfile():
    with open('KY.txt') as file:
        lines = file.readlines()
    print(lines)
    return lines;

def writetofile(list):
    filename = "emails.txt"
    f = open(filename, "w")
    for email in list:
        f.write(email+"\n")
    f.close()

def google_parse(search_string, start):
    print("Test")
    temp = []
    url = 'http://www.google.com/search'
    payload = {'q': search_string, 'start': start}
    user_agent = {'User-agent': 'Mozilla/11.0'}
    request_response = requests.get(url, params=payload, headers=user_agent)

    soup = BeautifulSoup(request_response.text, 'html.parser')
    aTags = soup.find_all('a')
    print(aTags)
    for a in aTags:
        try:
            temp.append(re.search('url\?q=(.+?)\&sa', a['href']).group(1))
        except:
            continue


    return temp

def main(search, pages):
    start = timer()
    result = []
    for page in range( 0,  int(pages) ):
        result.extend(google_parse( search, str(page*10) ) )
    result = list( set( result ) )
    result = removefalselinks(result)

    print( *result, sep = '\n' )
    print( '\nTotal URLs Scraped : %s ' % str( len( result ) ) )
    print( 'Script Execution Time : %s ' % ( timer() - start, ) )
    return result


def removefalselinks(pagelist):
    for page in pagelist:
        if 'http' in page:
            continue
        else:
            pagelist.remove(page)
    return pagelist

def scrapepages( pagelist ):
    emails = []
    for page in pagelist:
        print(page + ":")
        foundemails = finddata(page)
        if foundemails is None:
            continue
        for email in foundemails:
            emails.append(email)
    print(emails)
    return emails

def finddata( pageurl ):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/11.0'
    }
    try:
        print("Making Request")
        req = requests.get(pageurl, headers, timeout=5)
        print("Grabbing HTML")
        soup = BeautifulSoup(req.content, 'html.parser')
        print("Prettying up data")
        pagedata = soup.prettify()
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(regex, pagedata)
        print(emails)
        return emails
    except:
        print("Timeout")

def removeduplicates(emails):
    print(emails)
    return list(set(emails))

def validatelist(emails):
    newlist = removeduplicates(emails)
    emailfinal = []
    for email in newlist:
        if '.png' in email:
            print(email)
        elif '.jpeg' in email:
            print(email)
        else:
            emailfinal.append(email)
    return emailfinal

if __name__ == '__main__':
    businesses = readfile()
    scrapedEmails = []
    i = 0
    while i < 3000:
        i += 1
        for business in businesses:
            urls = main(business, 1)
            emails = scrapepages(urls)
            validatedlist = validatelist(emails)
            for email in validatedlist:
                scrapedEmails.append(email)
    print(scrapedEmails)
    writetofile(scrapedEmails)
    print("Done")


