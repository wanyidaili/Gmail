# dataClassifier.py
# -----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# This file contains feature extraction methods and harness
# code for data classification

import mostFrequent
import naiveBayes
import perceptron
import mira
import sys
import util
import gmail_data
import collections

 # email is a pandas.series: (["subejct", "body", "from", "to", "date"])
def basicFeatureExtractorEmail(email):
    """
    Basic features that I can think of...
    """
    features = util.Counter()
    # the appearance of words
    for i in email:
        if i == None:
            i = ""

    features["Wanyi"] = 1 if "Wanyi" in email[1] else 0

    features["time"] = 1 if "time" in email[1] else 0

    #features["thank"] = 1 if "thank" in email[1] else 0

    features["question"] = 1 if "question" in email[1] else 0

    features["can"] = 1 if "can" in email[1] else 0

    #features["please"] = 1 if "please" in email[1] else 0

    features["Hi Wanyi"] = 1 if "hi wanyi" in email[1] else 0

    features[":)"] = 1 if ":)" in email[1] else 0

    features["?"] = 1 if "?" in email[1] else 0

    #features["important"] = 1 if "important" in email[1] else 0

    features["could"] = 1 if "could" in email[1] else 0

    features["respond"] = 1 if "respond" in email[1] else 0

    #features["sorry"] = 1 if "sorry" in email[1] else 0

    #features["you"] = 1 if "you" in email[1] else 0

    features["free"] = 1 if "free" in email[1] else 0

    #features["will"] = 1 if "will" in email[1] else 0

    communicatedList = dfsent["to"].values
    features["communicated"] = 0
    if email[2] in communicatedList:
        features["communicated"] = 1

    counter = collections.Counter(communicatedList)
    frequentCommunicator = [i[0] for i in counter.most_common(15)]
    features["frequentCommunicator"] = 0
    if email[2] in frequentCommunicator:
        features["frequentCommunicator"] = 5

    features["receiverNotMe"] = 0
    if "wli2" not in email[2]:
        features["receiverNotMe"] = 1

    # features["lengthOfBody"] = 0
    # if len(email[1].split()) != 0:
    #     features["lengthOfBody"] = len(email[1].split())

    # features["lengthOfBodyShoterThan300"] = 0
    # if len(email[1].split()) <= 300:
    #     features["lengthOfBodyShoterThan300"] = 1

    return features

def enhancedFeatureExtractorEmail(email):
    """
    This is empty because all of my basic features are already enhanced.
    Anyone can add more if they want to.
    """
    features =  basicFeatureExtractorEmail(email)

    return features



def default(str):
    return str + ' [Default: %default]'

USAGE_STRING = """
  USAGE:      python dataClassifier.py <options>
  EXAMPLES:   (1) python dataClassifier.py
                  - trains the default mostFrequent classifier on the Email dataset
                  using the default 100 training examples and
                  then test the classifier on test data
              (2) python dataClassifier.py -c naiveBayes -d Emails -t 1000 -f -o -1 3 -2 6 -k 2.5
                  - would run the naive Bayes classifier on 1000 training examples
                  using the enhancedFeatureExtractorEmails function to get the features
                  on the faces dataset, would use the smoothing parameter equals to 2.5, would
                  test the classifier on the test data and performs an odd ratio analysis
                  with label1=3 vs. label2=6
                 """


def readCommand( argv ):
    "Processes the command used to run from the command line."
    from optparse import OptionParser
    parser = OptionParser(USAGE_STRING)

    parser.add_option('-c', '--classifier', help=default('The type of classifier'), choices=['mostFrequent', 'nb', 'naiveBayes', 'perceptron', 'mira', 'minicontest'], default='mostFrequent')
    parser.add_option('-d', '--data', help=default('Dataset to use'), choices=['emails'], default='emails')
    parser.add_option('-t', '--training', help=default('The size of the training set'), default=100, type="int")
    parser.add_option('-f', '--features', help=default('Whether to use enhanced features'), default=False, action="store_true")
    parser.add_option('-o', '--odds', help=default('Whether to compute odds ratios'), default=False, action="store_true")
    parser.add_option('-1', '--label1', help=default("First label in an odds ratio comparison"), default=0, type="int")
    parser.add_option('-2', '--label2', help=default("Second label in an odds ratio comparison"), default=1, type="int")
    parser.add_option('-w', '--weights', help=default('Whether to print weights'), default=False, action="store_true")
    parser.add_option('-k', '--smoothing', help=default("Smoothing parameter (ignored when using --autotune)"), type="float", default=2.0)
    parser.add_option('-a', '--autotune', help=default("Whether to automatically tune hyperparameters"), default=False, action="store_true")
    parser.add_option('-i', '--iterations', help=default("Maximum iterations to run training"), default=3, type="int")
    parser.add_option('-s', '--test', help=default("Amount of test data to use"), default=100, type="int")

    options, otherjunk = parser.parse_args(argv)
    if len(otherjunk) != 0: raise Exception('Command line input not understood: ' + str(otherjunk))
    args = {}

    # Set up variables according to the command line input.
    print "Doing classification"
    print "--------------------"
    print "data:\t\t" + options.data
    print "classifier:\t\t" + options.classifier
    if not options.classifier == 'minicontest':
        print "using enhanced features?:\t" + str(options.features)
    #print "training set size:\t" + str(options.training)
    if(options.data=="emails"):

        if (options.features):
            featureFunction = enhancedFeatureExtractorEmail
        else:
            featureFunction = basicFeatureExtractorEmail

    else:
        print "Unknown dataset", options.data
        print USAGE_STRING
        sys.exit(2)

    if(options.data=="emails"):
        legalLabels = [-1,1]


    if options.training <= 0:
        print "Training set size should be a positive integer (you provided: %d)" % options.training
        print USAGE_STRING
        sys.exit(2)

    if options.smoothing <= 0:
        print "Please provide a positive number for smoothing (you provided: %f)" % options.smoothing
        print USAGE_STRING
        sys.exit(2)

    if options.odds:
        if options.label1 not in legalLabels or options.label2 not in legalLabels:
            print "Didn't provide a legal labels for the odds ratio: (%d,%d)" % (options.label1, options.label2)
            print USAGE_STRING
            sys.exit(2)

    if(options.classifier == "mostFrequent"):
        classifier = mostFrequent.MostFrequentClassifier(legalLabels)
    elif(options.classifier == "naiveBayes" or options.classifier == "nb"):
        classifier = naiveBayes.NaiveBayesClassifier(legalLabels)
        classifier.setSmoothing(options.smoothing)
        if (options.autotune):
            print "using automatic tuning for naivebayes"
            classifier.automaticTuning = True
        else:
            print "using smoothing parameter k=%f for naivebayes" %  options.smoothing
    elif(options.classifier == "perceptron"):

        classifier = perceptron.PerceptronClassifier(legalLabels,options.iterations)

    elif(options.classifier == "mira"):
        classifier = mira.MiraClassifier(legalLabels, options.iterations)
        if (options.autotune):
            print "using automatic tuning for MIRA"
            classifier.automaticTuning = True
        else:
            print "using default C=0.001 for MIRA"

    else:
        print "Unknown classifier:", options.classifier
        print USAGE_STRING

        sys.exit(2)

    args['classifier'] = classifier
    args['featureFunction'] = featureFunction

    return args, options


def runClassifier(args, options):
    featureFunction = args['featureFunction']
    classifier = args['classifier']
    
    print "Loading data"

    numTraining = options.training
    numTest = options.test

    rawTrainingData = []
    trainingLabels = []
    rawValidationData = []
    validationLabels = []
    rawTestData = []
    testLabels = []

    for i in range(dftraining.shape[0]):
        rawTrainingData.append(dftraining.loc[i].values[:-1])
        trainingLabels.append(dftraining.loc[i].values[-1])
    for i in range(dfvalidation.shape[0]):
        rawValidationData.append(dfvalidation.loc[i].values[:-1])
        validationLabels.append(dfvalidation.loc[i].values[-1])
    for i in range(dftesting.shape[0]):
        rawTestData.append(dftesting.loc[i].values[:-1])
        testLabels.append(dftesting.loc[i].values[-1])

    # Extract features
    print "Extracting features..."
    trainingData = map(featureFunction, rawTrainingData)
    validationData = map(featureFunction, rawValidationData)
    testData = map(featureFunction, rawTestData)

    # Conduct training and testing
    print "Training..."
    classifier.train(trainingData, trainingLabels, validationData, validationLabels)
    print "Validating..."
    guesses = classifier.classify(validationData)
    correct = [guesses[i] == validationLabels[i] for i in range(len(validationLabels))].count(True)

    # # print out the emails that have been classified into the wrong label
    # print "The wrong emails are..."
    # for i in range(len(validationLabels)):
    #     if guesses[i] != validationLabels[i]:
    #         print rawValidationData[i]
    #         print "This email's correct label is", validationLabels[i]

    incorrect = [guesses[i] == validationLabels[i] for i in range(len(validationLabels))].count(False)
    truePositive = [guesses[i] == 1.0 and validationLabels[i] == 1.0 for i in range(len(validationLabels))].count(True)
    trueNegative = [guesses[i] == -1.0 and validationLabels[i] == -1.0 for i in range(len(validationLabels))].count(True)
    falsePositive = [guesses[i] == 1.0 and validationLabels[i] == -1.0 for i in range(len(validationLabels))].count(True)
    falseNegative = [guesses[i] == -1.0 and validationLabels[i] == 1.0 for i in range(len(validationLabels))].count(True)

    print "number of correct guesses are", correct
    print "number of incorrect guesses are", incorrect
    print "number of truePositive guesses are", truePositive
    print "number of trueNegative guesses are", trueNegative
    print "number of falsePositive guesses are", falsePositive
    print "number of falseNegative guesses are", falseNegative

    print str(correct), ("correct out of " + str(len(validationLabels)) + " (%.1f%%).") % (100.0 * correct / len(validationLabels))
    print "Testing..."
    guesses = classifier.classify(testData)
    correct = [guesses[i] == testLabels[i] for i in range(len(testLabels))].count(True)
    print str(correct), ("correct out of " + str(len(testLabels)) + " (%.1f%%).") % (100.0 * correct / len(testLabels))

    # do odds ratio computation if specified at command line
    if((options.odds) & (options.classifier == "naiveBayes" or (options.classifier == "nb")) ):
        label1, label2 = options.label1, options.label2
        features_odds = classifier.findHighOddsFeatures(label1,label2)
        if(options.classifier == "naiveBayes" or options.classifier == "nb"):
            string3 = "=== Features with highest odd ratio of label %d over label %d ===" % (label1, label2)
        else:
            string3 = "=== Features for which weight(label %d)-weight(label %d) is biggest ===" % (label1, label2)
        print string3

    if((options.weights) & (options.classifier == "perceptron")):
        for l in classifier.legalLabels:
            features_weights = classifier.findHighWeightFeatures(l)
            print ("=== Features with high weight for label %d ==="%l)


if __name__ == '__main__':
    # Read input
    args, options = readCommand( sys.argv[1:] )
    # Run classifier
    dfsent, dftraining, dfvalidation, dftesting = gmail_data.generate()
    runClassifier(args, options)

    a = collections.Counter(dftraining["label"])
    b = collections.Counter(dfvalidation["label"])
    c = collections.Counter(dftesting["label"])
    print "training data set has total %s emails and "%dftraining.shape[0], a
    print "validation data set has total %s emails and "%dfvalidation.shape[0], b
    print "testing data set has total %s emails and "%dftesting.shape[0], c

