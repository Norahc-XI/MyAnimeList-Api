import re
import requests
from bs4 import BeautifulSoup

class MyAnimeListAPI():
    def __init__(self, url):
        self.HTML=BeautifulSoup(requests.get(url).content, "html.parser")
        self.INFO=self.showinfo()
        self.titles=self.ReturnTitles(self.INFO)
        self.synopsis=self.HTML.find("p", {"itemprop":"description"}).text
        self.type=self.ReturnMacth("Type")
        self.episodes=self.ReturnMacth("Episodes")
        self.status=self.ReturnMacth("Status")
        self.aired=self.ReturnMacth("Aired")
        self.producers=self.ReturnMacth("Producers").replace(",", ", ")
        self.licensors=self.ReturnMacth("Licensors")
        self.studios=self.ReturnMacth("Studios").replace(",", ", ")
        self.source=self.ReturnMacth("Source")
        self.genres=self.ReturnGenres().replace(",", ", ")
        self.duration=self.ReturnMacth("Duration").replace("min.perep.", " min. per ep.")
        self.rating=self.ReturnMacth("Rating").replace("-", " - ")
        self.score=self.FilterScore(self.ReturnMacth("Score"))
        self.ranked=self.ReturnMacth("Ranked").replace("2basedonthetopanimepage.Pleasenotethat'Notyetaired'and'R18+'titlesareexcluded.", "")
        self.popularity=self.ReturnMacth("Popularity")
        self.members=self.ReturnMacth("Members")
        self.favorites=self.ReturnMacth("Favorites")
        self.__info__="Api no oficial del administrador de animes MyAnimeList"
        
    def showinfo(self):
        info=[]
        for i in self.HTML.find_all("div", {"class":"spaceit_pad"}):
            if i.text.replace("\n","")=="Main": break
            else: info.append(i.text.replace(" ","").replace("\n", "").replace(":", " : "))
        return info
    
    def ReturnTitles(self, array):
        titles=[]
        for i in array:
            if re.search("Type", i) is not None: break
            else: titles.append(i)
        return titles
    
    def ReturnGenres(self):
        for i in self.INFO: 
            if re.search("Genre*", i): return i
    
    def ReturnMacth(self, search):
        for i in self.INFO: 
            if re.search(search, i): return i
            
    def FilterScore(self, text):
        nums=[]
        for i in text:
            if i=="(": return "".join(nums)
            else: nums.append(i)