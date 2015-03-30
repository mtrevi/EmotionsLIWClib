<h2>EmotionsLIWClib</h2>

This is a python script that given a string, return the polarity of each sentence. It relies on the [Linguistic Inquiries and Word Count](http://www.liwc.net/descriptiontable1.php), that however, it is not available in this repository and it needs to be retrieved by other sources. 


------------
<h2>Example of Emotion Polarity Computation</h2>


```
from LIWClib.EmotionsLIWClib import *
myLIWC = LIWCObj()
myLIWC.build_model('LIWClib/dictionary/LIWC2007_English100131.dic')
myLIWC.unittest()
PASSED - ({'posemo': 0, 'negemo': 3}) This pasta sucks, it is made by shit. I don't like this pizza.
PASSED - ({'posemo': 0, 'negemo': 0}) Questa passata fa schifo!
PASSED - ({'posemo': 1, 'negemo': 2}) This restaurant has all my love but the food is not good and the service is terrible!
```
