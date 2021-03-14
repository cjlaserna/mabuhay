from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
  
X ="Nagbabaha dito kailangan namin na mga pagkain. Mad-donasyon po kayo at suporta at tulong ang pilinas sa kalamida na bagyo na ito."
Y ="Nagbabaha, kailangan, tulong, pagkain, rescue, emergency, bagyo, baha, tubig, donasyon, suporta"
  
# tokenization 
tweet_list = word_tokenize(X)  
mock_list= word_tokenize(Y) 

tweet_set = {w for w in tweet_list}
mock_set = {w for w in mock_list}

l1 =[];l2 =[] 
  
# remove stop words from the string 
  
rvector = tweet_set.union(mock_set)  
for w in rvector: 
    if w in tweet_set: l1.append(1) # vector 
    else: l1.append(0) 
    if w in mock_set: l2.append(1) 
    else: l2.append(0) 
c = 0
  
# cosine  
for i in range(len(rvector)): 
        c+= l1[i]*l2[i] 
cosine = c / float((sum(l1)*sum(l2))**0.5) 
print("similarity: ", cosine) 
