from bs4 import BeautifulSoup as bs
import re
import requests

fh = open("odd.csv",'w')
for i in range(1,97):
    print(f"Fetching page {i}")
    url = f"https://www.powerball.com/previous-results?gc=powerball&sd=1997-11-01&ed=2023-12-28&pg={i}"
    code = requests.request("GET", url)
    x = code.text
    soup = bs(x,'html.parser')
    odd = soup.text
    odd = odd.replace("\n\n","")
    odd = odd.replace("\\x\n","")
    odd = odd.replace("'Previous Results | Powerball\nSkip to content.\n      Powerball\n      \n               Games\n               \nPowerball\nLotto America\n2by2\nDouble Play               Results\n               \nPrevious Results\nCheck Your Numbers\nWatch the Drawing\nWinner Stories               More\n               \nLatest News\nMedia Center\nFAQs\nPrivacy Policy\nTerms & Conditions\nPlay Responsibly\nMerchandise\nNASCAR Powerball PlayoffPrevious Results\nAre you holding a winning ticket?\nGame Name\n2by2\nDouble Play\nLotto America\nPowerball","")
    odd = odd.replace("x\n", " ")
    odd = odd.replace("Previous Results | Powerball\nSkip to content.\n      Powerball\n      \n               Games\n               \nPowerball\nLotto America\n2by2\nDouble Play               Results\n               \nPrevious Results\nCheck Your Numbers\nWatch the Drawing\nWinner Stories               More\n               \nLatest News\nMedia Center\nFAQs\nPrivacy Policy\nTerms & Conditions\nPlay Responsibly\nMerchandise\nNASCAR Powerball PlayoffPrevious Results\nAre you holding a winning ticket?\nGame Name\n2by2\nDouble Play\nLotto America\nPowerball","")
    odd = odd.replace("    Power Play","\n")
    odd = odd.replace("    Power Play\n\t\t2 ","\n")
    odd = odd.replace("    Power Play\n\t\t3 ","\n")
    odd = odd.replace("    Power Play\n\t\t5 ","\n")
    odd = odd.replace("    Power Play\n\t\t10 ","\n")
    odd = odd.replace("    Power Play\n\t\t4 ","\n")
    odd = odd.replace("    Power Play\n\t\t2x","\n")
    odd = odd.replace("    Power Play\n\t\t3x","\n")
    odd = odd.replace("    Power Play\n\t\t4x","\n")
    odd = odd.replace("    Power Play\n\t\t5x","\n")
    odd = odd.replace("    Power Play\n\t\t10x","\n")
    odd = odd.replace("          Load More\n        PowerballMedia Center\nLegal\nPrivacy\nespañol      All winning tickets must be redeemed in the state/jurisdiction in which they are sold.\n      © Multi-State Lottery Association. All Rights Reserved.\n    \nWe use cookiesCookies help us deliver the best experience on our website. By using our website, you agree to the use of cookies. Find out how we use cookies.\nClose\nAccept","")
    odd = odd.replace("Start DateEnd DateSearch\nClear","")
    odd = odd.replace(", ","-")
    odd = odd.replace("\nM","&M")
    odd = odd.replace("\nT","&T")
    odd = odd.replace("\nW","&W")
    odd = odd.replace("\nS","&S")
    odd = odd.replace("\n",",")
    odd = odd.replace("&Mon","\nMon")
    odd = odd.replace("&Tue","\nTue")
    odd = odd.replace("&Wed","\nWed")
    odd = odd.replace("&Thu","\nThu")
    odd = odd.replace("&Fri","\nFri")
    odd = odd.replace("&Sat","\nSat")
    odd = odd.replace("&Sun","\nSun")
    pre = odd.split("\n")
    for ds in pre:
        dc = ds.split(",")[0].split("-")
        nums = ",".join(ds.split(",")[1:])
        rep = (re.search(r"(\d{4})(\d+)",dc[2]).groups())
        ns = f"{rep[0]},{rep[1]}"
        nsf = f"{dc[0]}-{dc[1]}-{ns}"
        post = f"{nsf},{nums}"
        fh.write(post.rstrip(","))
        fh.write("\n")
fh.close()
