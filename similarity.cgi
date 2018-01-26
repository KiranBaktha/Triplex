#!C:\Users\sunda\AppData\Local\Continuum\anaconda3\python.exe

import cgi
data = cgi.FieldStorage()



print ("Content-type: text/html")
print ()
print("<html>")
print("""
      <head>
          <title>Similar Sentences</title>  
      </head>
      """)
print("""
       <style>
 
 body{
 background-color:black
 }

 h2{
 text-align:center;
 color: white;
 margin-botton: 2%
 }
 
 .text_content{
 
height: 1200px;
width: 60%;
background-image: url('http://localhost/Old-Paper.gif');
background-repeat:no-repeat; 
background-size:contain;
position: absolute;
top: 50%;
left: 50%;
margin: -175px 0 0 -300px;
align-items: center;
justify-content: center;
}

.inner_text{
margin-top: 10%;
font-size: 12px;
width: 80%;
margin-left: 13%;
height: 350px;
overflow-y:scroll;
}
 
/* width */
::-webkit-scrollbar {
    width: 10px;
}

/* Track */
::-webkit-scrollbar-track {
    box-shadow: inset 0 0 8px black; 
    border-radius: 10px;
}
 
/* Handle */
::-webkit-scrollbar-thumb {
    background: #CC6600; 
    border-radius: 15px;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
    background: #b30000; 
}
 
 
 </style>
      """)

print("""<body>
<h2> SIMILAR SENTENCES </h2>
<div class = 'text_content'>
<p class = 'inner_text'>
""")

# Set path to access the stored nltk words.

import os
os.environ['APPDATA'] = "C:\\Users\\sunda\\AppData\\Roaming"

try:   # Check for any importing errors
    from bs4 import BeautifulSoup
    from bs4.element import Comment
    import urllib
    import re
    from nltk.corpus import stopwords
    from nltk.corpus import wordnet
    import string
    import itertools
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    stop = set(stopwords.words('english'))
except Exception as e:
    print(str(e))
    print("""</p>
          </div>  
          </body>
          </html>
          """)
    

headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'

def visible(element):
    """
    Function that removes non-visible text in webpage and comments from the html file.
    """
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    for sup in soup.find_all("sup", {'class':'reference'}): 
        sup.decompose()
    texts = soup.findAll(text=True)
    visible_texts = filter(visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

delimiters = "   ",". "  # Regex to remove punctuations.
regexPattern = '|'.join(map(re.escape, delimiters))


def return_dict(website):
    reqx = urllib.request.Request(website,headers = headers)
    htmlx = urllib.request.urlopen(reqx)
    content = text_from_html(htmlx)
    dictionary = {}
    d = re.split(regexPattern,content)
    for sentence in d:
        sen_modified = re.sub(regex,'',sentence)
        sentence_split = [word.lower() for word in sen_modified.split()]
        if len(sentence_split)>5 and len(sentence_split)<100:
            words= tuple(list(filter(lambda w: not w in stop,sentence_split)))
            if len(words) > 3:  # Sentence to have minimum 3 words to be considered.
                if words not in dictionary:
                    dictionary[words] = set([sentence.strip()])
                else:
                    dictionary[words].add(sentence.strip())
    return dictionary
    


website1 = str(data.getvalue("first_website"))
d1 = return_dict(website1)
website2 = str(data.getvalue("second_website"))
d2 = return_dict(website2)
website3 = str(data.getvalue("third_website"))
d3 = return_dict(website3)

synonyms = {}


def compute_Levenshtein_Distance(sen1,sen2):
    """
    Function that takes two sentences as arguments and returns the Levenshtein distance between them.
    Synonyms of words are accounted for using python's wordnet.
    """
    mat = [[[] for i in range(len(sen1)+1)] for i in range(len(sen2)+1)]
    for i in range(len(sen1)+1):
        mat[0][i] = i
    for j in range(len(sen2) + 1):
        mat[j][0] = j
    for i in range(1,len(sen2)+1):
        for j in range(1,len(sen1)+1):
            cost = 1
            if sen1[j-1] not in synonyms:
                sy = [[name.name() for name in x.lemmas()] for x in wordnet.synsets(sen1[j-1])]  # Store synonyms
                synonyms[sen1[j-1]] = set(itertools.chain.from_iterable(sy))
            if sen2[i-1] in synonyms[sen1[j-1]] or sen2[i-1]==sen1[j-1]:
                cost = 0
            mat[i][j] = min(mat[i-1][j-1]+cost,mat[i-1][j]+1,mat[i][j-1]+1)
    return mat[len(sen2)][len(sen1)]



result1 = set()
for key1 in d2:
    for key2 in d1:
        if compute_Levenshtein_Distance(key1,key2) <= 5:  # Distance check
            result1.add(key1)
            result1.add(key2)
            
result2 = set()
for key1 in result1:
    for key2 in d3:
        if compute_Levenshtein_Distance(key1,key2) <= 5:  # Distance check
            result2.add(key1)
            result2.add(key2)

if len(result2)==0:  # If no sentences match.
    print("No Sentences match the given criteria!")

# Print the sentences from their respective websites.
for key in result2:
    try:
        for sentence in d1[key]:
            print(sentence)
            print("<br>")
    except:
        try:
            for sentence in d2[key]:
                print(sentence)
                print("<br>")
        except:
            try:
                for sentence in d3[key]:
                    print(sentence)
                    print("<br>")
            except:
                pass


print("""</p>
</div>  
</body>
</html>
      """)
