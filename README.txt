README.txt
Two main files that contains the most important part of the code is gmail_data.py, dataClassifier.py and perceptron.py.
gmail_data.py uses pandas to create DataFrames that contain information about emails including their subject, body, sender, receiver and date. It also identifies which incoming emails have been replied or not. A binary value is stored as "label" in the DataFrames for training, validation and testing sets.
dataClassifier.py is a modified file from the CS232 Project 4. The file is adjusted to do data classification for emails. The method BasicFeatureExtraction contains a list of features that I designed. The method runClassifier is also largely modified to produce the data structures for the emails and to print appropriate results.
perceptron.py contains the perceptron algorithm of the project.
The rest of the files are not deleted because it is possible to extend this project to beyond only using perceptron. Mira and naiveBayes are also potential algorithms, but not yet ready.

User Manual:
Since my result all come from my personal email account, my data is not shared here. Go to "My Account" through Google and choose "personal info & privacy" tab. Scroll down you will see the option to "Create Archive". Then download your gmail data (it will come in mbox format). Create an archive for your inbox and rename it to be "Inbox.mbox", then a sperate archive for your sent box and rename it to be "Sent.mbox". Put both files into the same folder with this. Then you are all set.

Simply type in command line: python dataClassifier.py -c perceptron

You can contribute to the project by adding your own features into the enhancedFeatureExtraction method in dataClassifier.py.

Sample output:
'''
Doing classification
--------------------
data:       emails
classifier:     perceptron
using enhanced features?:   False
Finished storing subjects from sent emails.
Finished creating inbox database with labels
Loading data
Extracting features...
Training...
Starting iteration  0 ...
Starting iteration  1 ...
Starting iteration  2 ...
After the training, weights have become:  {1: {'respond': 0, 'receiverNotMe': -3, 'Hi Wanyi': 0, 'could': 2, 'question': 1, 'free': 1, 'frequentCommunicator': 5, 'Wanyi': 5, 'can': -1, 'time': -1, 'communicated': 1, '?': -1, ':)': 0}, -1: {'respond': 0, 'receiverNotMe': 3, 'Hi Wanyi': 0, 'could': -2, 'question': -1, 'free': -1, 'frequentCommunicator': -5, 'Wanyi': -5, 'can': 1, 'time': 1, 'communicated': -1, '?': 1, ':)': 0}}
Validating...
number of correct guesses are 187
number of incorrect guesses are 58
number of truePositive guesses are 46
number of trueNegative guesses are 141
number of falsePositive guesses are 56
number of falseNegative guesses are 2
187 correct out of 245 (76.3%).
Testing...
66 correct out of 79 (83.5%).
training data set has total 144 emails and  Counter({-1.0: 125, 1.0: 19})
validation data set has total 245 emails and  Counter({-1.0: 197, 1.0: 48})
testing data set has total 79 emails and  Counter({-1.0: 67, 1.0: 12})
'''