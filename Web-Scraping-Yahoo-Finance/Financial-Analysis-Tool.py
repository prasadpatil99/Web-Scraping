from bs4 import BeautifulSoup
import pandas as pd
import requests
import warnings
warnings.filterwarnings("ignore")

def world_derivatives(url):
    
    wd_url = "https://in.finance.yahoo.com/"+url
    req= requests.get(wd_url)
    data=req.text
    soup=BeautifulSoup(data)
    
    symbl_names=[]
    prices=[]
    changes=[]
    perchngs=[]
    	
    for i in range(1):
       for body in soup.find_all('tbody'):
          for row in body.find_all('tr'):
             for name in row.find_all('td', attrs={'class':'data-col1'}):
                symbl_names.append(name.text)
             for price in row.find_all('td', attrs={'class':'data-col2'}):
                prices.append(price.text)
             for change in row.find_all('td', attrs={'class':'data-col3'}):
                changes.append(change.text)
             for perchng in row.find_all('td', attrs={'class':'data-col4'}):
                perchngs.append(perchng.text)
                
    df = pd.DataFrame({"Names": symbl_names, "Prices": prices, "Change": changes, "Change in %": perchngs})
    return df


def eq_stocks():

    print("\nStock Analysis")
    choice1 = int(input("\n1.Stocks:Most Active\n2.Stocks:Gainers\n3.Stocks:Losers\n\nEnter Input:"))
    
    def inpt(choice1):
        switcher={    
        1:'most-active',    
        2:'gainers',    
        3:'losers'   
        }    
    
        return switcher.get(choice1)
        
    url = inpt(choice1)
    
    cnt = int(input("Enter Number of Entries Required:"))
    
    res = requests.get("https://in.finance.yahoo.com/"+url)
    soup = BeautifulSoup(res.content,'lxml')
    table = soup.find_all('table')[0] 
    df = pd.read_html(str(table))[0]
    names = df["Name"].tolist()
    prices = df["Price (intraday)"].tolist()
    changes = df["Change"].tolist()
    per_Change = df["% change"].tolist()
                
    df = pd.DataFrame({'Names':names,'Prices':prices, 'Changes':changes, 'Per_Change':per_Change})
    df = df.loc[:(cnt-1)]
    
    return df

def news():
    
    tags=[]
    
    res = requests.get("https://in.finance.yahoo.com/topic/latestnews")
    soup = BeautifulSoup(res.text, 'html.parser')
    
    collection = soup.findAll("img")
    for img in collection:
        if 'alt' in img.attrs:
            tags.append(img.attrs['alt'])
            
    return tags


choice = int(input("Enter Derivative Required\n1.Currencies\n2.World Indices\n3.Commodities\n4.Equity Market Analysis\n5.Market News\n\nEnter Input By Index:"))

if(1<=choice<=3):
    
    def inpt(choice):
        switcher={    
        1:'currencies',    
        2:'world-indices',    
        3:'commodities'
        }    
        return switcher.get(choice)

    url = inpt(choice)

    print(world_derivatives(url))

elif(choice==4):
    eq = eq_stocks()
    print(eq)
    cv = input('Do you want to save this in csv file?:\ny or n:')
    if(cv=="y"):
        eq.to_csv('file.csv') 
    else:
        exit()

elif(choice==5):
    n = news()
    for _ in n:
        print(_,end='\n')
    
elif(choice==0 or choice>=6):
    print('Invalid Entry')
    exit()
