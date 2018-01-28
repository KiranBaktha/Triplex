# Triplex
A web application that displays top 3 websites in google search in parallel. Also shows similar sentences in them computed using the Levenshtein distance metric.  <br/>
The computation time varies on the server capabilities and the websites searched for. <br/> 
Most websites block iframe tags in html from accessing them. So, I download the pages source code, handle issues like relative/absolute paths and display them in the iframe. <br/>
Since this was intended for my personal use I have not created database functionality. <br/>
Sentence Segmentation is performed on  "period+space" and "> single space"


![StartPage](https://github.com/KiranBaktha/Triplex/blob/master/Start%20Page.png)

