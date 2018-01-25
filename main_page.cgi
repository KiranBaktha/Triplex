#!C:\Users\sunda\AppData\Local\Continuum\anaconda3\python.exe

import cgi
import os
import urllib
from urllib.parse import urljoin
import urllib.parse
from bs4 import BeautifulSoup


data = cgi.FieldStorage()  # Access sent input text file
ent = data.getvalue("textt")
user = 'mark'  # Just a random username. I have not enabled MySQL capabilites to create new users because this was for personal use.
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'

def get_html(ent):
    """
    Function that returns the raw html of the google search page searched with phrase 'ent'.
    """
    try:
        values = {'q' : ent}
        ent = urllib.parse.urlencode(values)
        url = "https://www.google.com/search?{}".format(ent)
        req = urllib.request.Request(url, headers = headers)
        html = urllib.request.urlopen(req)              
        return html
    except:
        print("Error fetching {}".format(ent))


html = get_html(str(ent))
page = BeautifulSoup(html,'html.parser')

links = []   # Datastructure to store top links
for idx,link in enumerate(page.findAll('div',attrs={'class':"rc"})):
    if not 'youtube' in str(link.a["href"]):  # Avoid Youtube links
        links.append(str(link.a["href"]))

links = list(set(links))  # Incase a website is in the feature snippet it appears twice so I am removing it.

print ("Content-type: text/html")
print ()
print ("<html>")
print ("<head>")
print ("<title>Worker</title>")
print("""<style>
#first{
background-color: red;
color: white;
font-family:verdana;
height: 70px;
margin-bottom: 0.7cm;
}
#frame_enclosure{
    width: 330px;
    height:800px;
    position:relative;
}
.frame{
    width: 100%;
    height:100%;
    border:3px solid red;
}
.expand{
    position:absolute;
    dispay: inline-block;
    font-family:"Comic Sans MS", cursive, sans-serif; 
    padding: 0px 20px; 
    text-decoration : none;
    color: #BEBFA;
    top:-23px;
    left:40px;
    width:80%;
    height:20px;
    margin:auto;
    }
    
.similar{
   position:relative;
   float:right;
   top:-20px;
   border:1px solid grey;
   height: 30px;
   }
    
</style>""")
    
print("""
   <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
      """)

print ("</head>")
print ("<body>")

print("<script>")
print("sessionStorage.setItem('{}', '{}');".format("first_website",links[0]))
print("sessionStorage.setItem('{}', '{}');".format("second_website",links[1]))
print("sessionStorage.setItem('{}', '{}');".format("third_website",links[2]))
print("</script>")


print("""
<div id = "first">
<h1 align = "center">TRIPLEX</h1>
""")

print("<button type = 'button' class = 'similar' onclick = 'location.href = \"http://localhost/similarity.cgi?first_website={};second_website={};third_website={}\";' style = 'background-color: black;'>View Similar Sentences</button>".format(links[0],links[1],links[2]))

print("</div>")

for i in range(3):
    name = user + str(i) + '.html'
    try:  # Delete file if it already exists
        os.remove(name)
    except OSError:
        pass
    reqx = urllib.request.Request(links[i], headers = headers)
    htmlx = urllib.request.urlopen(reqx)
    pagex = BeautifulSoup(htmlx,'html.parser')   # Convert relative to absolute links
    for url in pagex.find_all('img'):
        url['src'] = urljoin(links[i],url.get('src'))
        try:
            url['srcset'] = ','.join([urljoin(links[i],x.strip()) for x in url['srcset'].split(',')])
        except:
            pass
    for url in pagex.findAll('link', {'rel' : 'stylesheet'}): 
        url['href'] = urljoin(links[i],url.get('href'))
    for url in pagex.find_all('link'):
        url['href'] = urljoin(links[i],url.get('href'))
    for url in pagex.find_all('base'):
        url['href'] = urljoin(links[i],url.get('href'))
    for url in pagex.find_all('script'):
        url['src'] = urljoin(links[i],url.get('src'))
    pagex = pagex.encode('utf-8')
    with open(name,'wb')  as file:
        file.write(pagex)
    print("""<div class="col-sm-4" id = "frame_enclosure">""")   #Load iframe content from stored website (this way helps to load websites which have X-FRAME options set).
    print("""<iframe class = "frame" style = "margin-left: 5px;" src="http://localhost/{}"></iframe>""".format(name))
    if i==0:
        print("""<button  type = "button" class  = "expand" onclick = "location.href=sessionStorage.getItem('first_website');" >Expand </button>""")
    if i==1:
        print("""<button  type = "button" class  = "expand" onclick = "location.href=sessionStorage.getItem('second_website');" >Expand </button>""")
    if i==2:
        print("""<button  type = "button" class  = "expand" onclick = "location.href=sessionStorage.getItem('third_website');" >Expand </button>""")
    print("</div>")

print ("</body>")
print ("</html>")
