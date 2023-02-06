# Left Chart (WordCloud)
Use dropdown menu to choose the wordcloud for specific person (i.e. Moderator, Trump, and Biden).
The bigger the word the more it is used by that person and the occurence of the word is correlated with the color. The darker the color the more it is used.

In addition, when the mouse hover over the text, it will prompt you the number of occurence of that word, the polarity of that word, and the subjectivity of that word.

Most of the word's polarity and subjectivity is 0, I concluded that this is because the TextBlob module is not so good in classifying a single word. However, some of the words that has clear polarity and subjectivity, then the value will be shown; otherwise, the value is 0, which I conclude as netural under this context. Due to the aforemention issue, the color scale can't be incoprated into the scheme as it will mees up the readability.

From the moderator's wordcloud, we can see that the most frequenct used word is president and this is pretty obvious as he are constantly asking two people question and asking them to stop at what they are doing. And for Trump and Biden's wordcloud, they both use the word 'People' a lot. 

# Right Chart (Group Bar Chart)
Use dropdown menu to choose which topic to see the emotion breakdwon.

X-axis is the emotion category, namely, Happy, Sad, Surprise, Angry, and Fear.
Y-axis is the score indicating that each person's emotion in each category.

Due to the long classification time using text2Emotion, I saved the classification output into several csv files in `./server/data` for quick chart rendering.

Interestingly, for all three people in this debate, they all somehow show fear in their sentences.