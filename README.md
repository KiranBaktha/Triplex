# Triplex
A web application that displays top 3 websites in google search in parallel. Also shows similar sentences in them computed using the Levenshtein distance metric.  <br/>
The computation time varies on the server capabilities and the websites searched for. <br/> 
Most websites block iframe tags in html from accessing them. So, I download the pages source code, handle issues like relative/absolute paths and display them in the iframe. <br/>
Since this was intended for my personal use I have not created database functionality. <br/>

For sentence similarity, sentence segmentation is performed on  "period+space" and "> single space". Punctuationas are removed but numbers in sentences are kept. Stop words are removed using Python's nltk package. Synonyms of words are considered using Python's WordNet. [Levenshtein Distance](https://en.wikipedia.org/wiki/Levenshtein_distance) metric is used for measuring sentence similarity. <br/>

Here are the screenshots of the application on my device.<br/>
<br/>
This is the start page with the keyword to be search = "science".
<br/>
![StartPage](https://github.com/KiranBaktha/Triplex/blob/master/Start%20Page.png)

<br/>
This is the main page with the top 3 websites returned by google in parallel on the same webpage.
<br/>

![MainPage](https://github.com/KiranBaktha/Triplex/blob/master/Main%20Page.png)

<br/>

<br/>
The similar distances returned by the application.

<br/>

![SimilarityPage](https://github.com/KiranBaktha/Triplex/blob/master/Similar%20Sentences%20Page.png)

<br/>

