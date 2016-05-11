#-*-coding:UTF-8-*-
from numpy import *
import re

def loadDataSet(): #生成原始的训练文档和类别文档
	postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
				   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
	               ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
	               ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
	               ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
	classVec = [0, 1, 0, 1, 0, 1]
	return postingList, classVec


def createVocabList(dataSet): #根据训练文档生成词汇表
	vocabSet = set([])
	for document in dataSet:
		vocabSet = vocabSet | set(document)
	return list(vocabSet)


def setOfWords2Vec(vocabList, inputSet): #将文档根据词汇表进行向量化，这里是用的词集模型
	returnVec = [0]*len(vocabList)
	for word in inputSet:
		if word in vocabList:
			returnVec[vocabList.index(word)] = 1
		else:
			print "the word: %s is not in my Vocabulary!" % word
	return returnVec


def bagOfWords2VecMN(vocabList, inputSet): #将文档根据词汇表进行向量化，这里是用的词袋模型
	returnVec = [0]*len(vocabList)
	for word in inputSet:
		if word in vocabList:
			returnVec[vocabList.index(word)] += 1 #要考虑单词出现的次数
		else:
		    print "the word: %s is not in my Vocabulary!" % word
	return returnVec


def trainNB0(trainMatrix, trainCategory): #根据训练文档训练分类器参数
	numTrainDocs = len(trainCategory) #训练文档的总数
	numWords = len(trainMatrix[0]) #这里的训练文档实际上已经被向量化的文档，这里表示词汇表的长度
	pAbusive = sum(trainCategory)/float(numTrainDocs) #表示p(A)的概率，即侮辱性文档
	p0Num = ones(numWords); p1Num = ones(numWords) #词向量，用来计算p(wi|c0)和p(wi|c1)
	p0Denom = 2.0; p1Denom = 2.0 #用来计算每一类文档中的单词的总数
	for i in range(numTrainDocs):
		if trainCategory[i] == 1: #侮辱性文档
			p1Num += trainMatrix[i]
			p1Denom += sum(trainMatrix[i])
		else: #非侮辱性文档
			p0Num += trainMatrix[i]
			p0Denom += sum(trainMatrix[i])
	p1Vect = log(p1Num/p1Denom); p0Vect = log(p0Num/p0Denom)
	return p0Vect, p1Vect, pAbusive


def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1): #分类器将输入的文档进行分类
	p1 = sum(vec2Classify * p1Vec) + log(pClass1)
	p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
	if p1 > p0:
		return 1
	else:
		return 0


def testingNB(): #进行测试的函数
	listOPosts, listClasses = loadDataSet()
	myVocabList = createVocabList(listOPosts)
	trainMat = []
	for postinDoc in listOPosts:
		trainMat.append(setOfWords2Vec(myVocabList, postinDoc))

	'''标准安装的Python中用列表(list)保存一组值，可以用来当作数组使用，不过由于列表的元素可以是任何对象，因此列表中所保存的是对象的指针。这样为了保存一个简单的[1,2,3]，需要有3个指针和三个整数对象。对于数值运算来说这种结构显然比较浪费内存和CPU计算时间。
此外Python还提供了一个array模块，array对象和列表不同，它直接保存数值，和C语言的一维数组比较类似。但是由于它不支持多维，也没有各种运算函数，因此也不适合做数值运算。
因此下面将list先转换成numpy中的array数组。
	'''
	p0V, p1V, pAb = trainNB0(array(trainMat), array(listClasses))

	testEntry = ['love', 'my', 'dalmation']
	thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
	print testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb)
	testEntry = ['stupid', 'garbage']
	thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
	print testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb)


def textParse(bigString): #将文档解析成词向量
	listOfTokens = re.split(r'\W*', bigString)
	return [tok.lower() for tok in listOfTokens if len(tok) > 2] #这个是列表生成器


def spamTest(): #检测垃圾邮件
	docList=[]; classList = []; fullText =[]
	for i in range(1,26): #生成原始的词向量文档
		wordList = textParse(open('/home/leowang/Machine Learning/machinelearninginaction/Ch04/email/spam/%d.txt' % i).read())
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(1)
		wordList = textParse(open('/home/leowang/Machine Learning/machinelearninginaction/Ch04/email/ham/%d.txt' % i).read())
		docList.append(wordList) 
		fullText.extend(wordList)
		classList.append(0)

	vocabList = createVocabList(docList) #生成词汇表

	trainingSet = range(50); testSet=[] #下面随机生成训练集和测试集的序号
	for i in range(10):
		randIndex = int(random.uniform(0,len(trainingSet)))
		testSet.append(trainingSet[randIndex])
		del(trainingSet[randIndex])

	trainMat = []; trainClasses = [] #这里生成具体的训练集
	for docIndex in trainingSet:
		trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
		trainClasses.append(classList[docIndex])

	p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses)) #训练分类器

	errorCount = 0
	for docIndex in testSet:        #检验分类器的效果
		wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
		if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
			errorCount += 1
			print "classification error",docList[docIndex] #将分类出错的文档打印出来
	print 'the error rate is: ',float(errorCount)/len(testSet) #打印错误率
