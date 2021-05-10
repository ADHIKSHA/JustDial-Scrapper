from bs4 import BeautifulSoup
import urllib
import urllib.request
import requests
import csv


def innerHTML(element):
    return element.decode_contents(formatter="html")

def get_name(body):
	return soup.find('span', {'class':'fn'}).text

def which_digit(html):
    mappingDict={'icon-ji':9,
                'icon-dc':'+',
                'icon-fe':'(',
                'icon-hg':')',
                'icon-ba':'-',
                'icon-lk':8,
                'icon-nm':7,
                'icon-po':6,
                'icon-rq':5,
                'icon-ts':4,
                'icon-vu':3,
                'icon-wx':2,
                'icon-yz':1,
                'icon-acb':0,
                }
    return mappingDict.get(html,'')

def get_phone_number(body):
    phoneNo = []
    try: 
        for item in body.find_all('p',{'class':'contact-info'}):
            phone=''
            try:
            	for element in item.find_all(class_=True):
            		classes = []
            		classes.extend(element["class"])
            		phone+=str((which_digit(classes[1])))
            	phoneNo.append(phone)
            except:
            	pass
    except:
        pass
    return phoneNo


def get_rating(body):
	text=''
	if(body.find('span', {'class':'value-titles'})!=None):
		text = body.find('span', {'class':'value-titles'}).text
	return text

def get_rating_count(body):
	text=''
	if(body.find('span', {'class':'votes'})!=None):
		text = body.find('span', {'class':'votes'}).text
	return text

def get_address(body):
	val="None"
	i=0
	for x in body.select("span.lng_add"):
		i+=1
		if i==3:
			val=x.text
			break
	return val

def get_hours(body):
	val=''
	x = body.find('span','mreinflispn2')
	if(x!=None):
		val= x.text
	return val

def get_location(body):
	val="None"
	i=0
	for x in body.select("span.lng_add"):
		i+=1
		if i==1:
			val=x.text.strip()
			break
	return val

def get_website(body):
	ans="None"
	x = body.find_all('span', 'mreinfp comp-text')
	for i in x:
		val = i.find_all('a',href=True)
		for j in val:
			ans = j['href']
	return ans

page_number = 1
service_count = 1


fields = ['Name', 'PhoneNumber', 'Rating', 'Number of Ratings by Users', 'Address', 'Location','Hours','href','Website']
out_file = open('DataScrapping.csv','w')
csvwriter = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)
csvwriter.writeheader()
while True:
	if page_number > 50:
		break

	url="https://www.justdial.com/Mumbai/Carpenters/nct-10080635/page-%s" % (page_number)
	req = urllib.request.Request(url, headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"}) 
	page = urllib.request.urlopen( req )
	soup = BeautifulSoup(page.read(), "html.parser")
	services = soup.find_all('li', {'class': 'cntanr'})
	dict_service = {}
	for service_html in services:
		href = service_html.attrs.get('data-href')
		print(href)
		li= {}
		li['phoneNumber'] = get_phone_number(service_html)
		if href!=None:
			dict_service[href] = li

	for key,value in dict_service.items():
		req = urllib.request.Request(key, headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"})
		page = urllib.request.urlopen( req )
		soup = BeautifulSoup(page.read(), "html.parser")
		services = soup.find_all('ul', {'class': 'comp-contact'})
		name = get_name(soup)
		final={}
		final['href']=str(key)
		final['PhoneNumber']=str(dict_service[key]['phoneNumber'])
		Location= get_location(soup)
		rating = get_rating(soup)
		count = get_rating_count(soup)
		address = get_address(soup)
		hours = get_hours(soup)
		website = get_website(soup)

		if name != None:
			final['Name'] = name
		if rating != None:
			final['Rating'] = str(rating)
		if count != None:
			final['Number of Ratings by Users'] = str(count)
		if address != None:
			final['Address'] = str(address)
		if hours != None:
			final['Hours'] = str(hours)
		if Location != None:
			final['Location'] = str(Location)
		if website != None:
			final['Website'] = str(website)

		csvwriter.writerow(final)

		service_count += 1

	page_number += 1

out_file.close()