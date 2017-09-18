
import pandas as pd
import numpy as np
import collections
import pickle
import tensorflow as tf
import tflearn
import tflearn.data_utils as du
from tflearn.data_utils import to_categorical, pad_sequences
from tflearn.datasets import imdb
import utils.data_util as util

# Dataset loading
#trainX, trainY = du.load_csv( filepath='../../data/addr/tmp.txt', target_column=-1, has_header=True, categorical_labels=True, n_classes=20)

#testX, testY = du.load_csv( filepath='../../data/addr/tmp1.txt', target_column=-1, has_header=True, categorical_labels=True, n_classes=20)


def load_data(file):
  '''
	info:
		takes file name and use custom method to read adddress data from name-value pair.
		Name and value is seperated by tab and every line is record.
	input:
		filename: file name in form of string
		dataX: feature vector
	output:
		dataY: target
        
  '''
  window = 3
  dataX = []
  dataY = []
  septag = ['UNK' for x in range(window)]
  cur = []

  with open(file,'rb') as fd:
    for count,line in enumerate(fd):
      line = line.strip() 
      match = re.match( r'^$',line,re.M|re.I)
      if match:
         cur = [] 
         for 
         cur.append(
  idata = pd.read_csv(file,sep='\t')
  ll = len(idata)
  print("Processing {} file, Rec to process {}".format(file,ll))
  cnt=window
  for row in idata.iterrows():
     if cnt >= ll-1:
     #if cnt >= 20-1:
       break
     dataX.append([idata.val[cnt-1],idata.val[cnt],idata.val[cnt+1]])
     #dataX.append(idata.val[cnt])
     dataY.append(idata.tag[cnt])
     #print(idata.val[cnt-1],idata.val[cnt],idata.val[cnt+1],idata.tag[cnt])
     cnt += 1

  print("loaded {} X {} Y ".format(len(dataX),len(dataY)))
  return dataX,dataY

class Vocab:

  def createVocab(self):
    '''
  	input:
  		idata: raw data records
  	output:
  		cntr: Counter object of words
  		word2idx: word to id dictionary
  		idx2word: id to word ditionary
    '''
    self.cntr = collections.Counter()
    
    for i in range(len(self.data)):
      if type(self.data[i]) is list:
        for word in self.data[i]:
          self.cntr[word] += 1
      else:
         self.cntr[self.data[i]] += 1
    
    self.dict_size = len(self.cntr)
    print("Total words in data set: ", self.dict_size)

    #truncate vocab of data to carry fwd just 10% of top dictinary words
    if self.dict_size > 100:
      self.dict_size = int(round(self.dict_size/10))
      print("Words dictionary truncated to: ", self.dict_size)
  
    self.vocab = sorted(self.cntr, key=self.cntr.get, reverse=True)[:self.dict_size]
    
    #Add not in vocab tag and update dict_size
    self.vocab.append(self.UNK)
    self.dict_size = len(self.vocab)
    print(self.vocab[:60])
    print('#no of time last word from vocab: ',self.vocab[-1], ': ', self.cntr[self.vocab[-1]])
    '''
    print('#no of time 500 th word from vocab: ',self.vocab[500], ': ', self.cntr[self.vocab[500]])
    print('#no of time 1000 th word from vocab: ',self.vocab[1000], ': ', self.cntr[self.vocab[1000]])
    print('#no of time 2000 th word from vocab: ',self.vocab[2000], ': ', self.cntr[self.vocab[2000]])
    print('#no of time 3000 th word from vocab: ',self.vocab[3000], ': ', self.cntr[self.vocab[3000]])
    print('#no of time 4000 th word from vocab: ',self.vocab[4000], ': ', self.cntr[self.vocab[4000]])
    '''
    self.word2idx = {}
    for i,word in enumerate(self.vocab):
       self.word2idx[word] = i
    print('few keys of word2idx :',{k: self.word2idx[k] for k in self.word2idx.keys()[:5]})
  
    self.idx2word = dict((v, k) for k, v in self.word2idx.items()) 
    print('few keys of idx2word :',{k: self.idx2word[k] for k in self.idx2word.keys()[:5]})
   
  def __init__(self,idata):
     self.data = idata
     self.vocab = []
     self.word2idx = {}
     self.idx2word = {}
     self.cntr = None
     self.UNK = 'IG'
     self.createVocab()

  def convData(self,data):
     rawdata = []
     for i in range(len(data)):
       if type(data[i]) is list:
         for word in data[i]:
           rawdata.append(word) 
       else:
         rawdata.append(data[i]) 

     return rawdata

  def getData(self):
     rawdata = []
     for i in range(len(self.data)):
       if type(self.data[i]) is list:
         for word in self.data[i]:
           rawdata.append(word) 
       else:
         rawdata.append(self.data[i]) 

     return rawdata

  def encode(self,data):
     codes = []
     for i in range(len(data)):
       if type(data[i]) is list:
         r_code = []
         for word in data[i]:
           #code  = self.word2idx.get(word)
           #if self.word2idx.has_key(word) == False:
           #  print("word missing in dict: ",word)
           #print(word,code)
           r_code.append(self.word2idx.get(word,self.word2idx.get(self.UNK))) 
         codes.append(r_code)
       else:
         codes.append(self.word2idx.get(data[i],self.word2idx.get(self.UNK))) 

     return codes

  def setUNK(self,UNK):
    self.UNK = UNK

  def getCodedData(self):
     codes = []
     for i in range(len(self.data)):
       if type(self.data[i]) is list:
         r_code = []
         for word in self.data[i]:
           #code  = self.word2idx.get(word)
           #print(word,code)
           r_code.append(self.word2idx.get(word,self.word2idx.get(self.UNK))) 
         codes.append(r_code)
       else:
         codes.append(self.word2idx.get(self.data[i],self.word2idx.get(self.UNK))) 

     return codes

  def updateVocab(self,upd_data):
    '''
  	input:
  		upd_data: raw data records
  	output:
  		cntr: Counter object of words
  		word2idx: word to id dictionary
  		idx2word: id to word ditionary
    '''
    for i in range(len(upd_data)):
      for word in upd_data[i]:
        self.cntr[word] += 1
        if self.word2idx.has_key(word) == False:
          self.vocab = self.vocab.append(word) 
          idx = len(self.word2idx) + 1
          self.word2idx[word] = idx
          self.idx2word[idx] = word
    


class Result:
  def __init__(self,test_data,y,pred,data_vocab,label_vocab):
    self.test_data = test_data
    self.y = y
    self.pred = pred
    self.data_vocab = data_vocab
    self.label_vocab = label_vocab
    self.processResult()

  def processResult(self):
    self.pred_code = np.argmax(self.pred,axis=1)
    self.pred_prob = np.amax(self.pred,axis=1)
    correct_prediction = tf.equal(tf.argmax(self.pred, 1), tf.argmax(self.y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    self.printAccuracy()
    #print('Acc type: ',type(accuracy))
    #print('Acc len: ',len(accuracy))
    #with open('accu.pkl','wb') as f1:
    #  pickle.dump(accuracy,f1)

  def printAccuracy(self):
    sep = '|'
    diff = {}
    with open('diff.txt','w') as f1:
      f1.write('rec' + sep + 'n-1' + sep + 'n' + sep + 'n+1' + sep + 'y' + sep + 'yhat' + '\n')
      for i,j in enumerate(self.pred_code):
        if self.label_vocab.idx2word[self.y[i]] != self.label_vocab.idx2word[j]:
        #if j != self.y[i]:
          diff[i] = j
          f1.write(
               str(i) + sep 
             + self.data_vocab.idx2word[self.test_data[i][0]] + sep 
             + self.data_vocab.idx2word[self.test_data[i][1]] + sep 
             + self.data_vocab.idx2word[self.test_data[i][2]] + sep 
             + self.label_vocab.idx2word[self.y[i]] + sep 
             + self.label_vocab.idx2word[j]+ '\n')
       
    self.accu = float(len(diff)/len(self.pred_code)) 
    print(" size {} errors {} Accuracy: {}".format(len(self.pred_code),len(diff),self.accu)) 

filepath='../data/addr/tmp.txt'
#trainX, trainY = load_data(filepath)
trainX, trainY = util.getToeknizeData(filepath,window=3)

err 

vocab = Vocab(trainX)
labels = Vocab(trainY)
labels.setUNK('UNK1')

Xdata = vocab.getCodedData()
Ydata = labels.getCodedData()

print("Coded X {} data: {}".format(len(Xdata),vocab.getData()[:10]))
print("Coded X code: {}".format(Xdata[:10]))
print("Coded Y size {} unique {} data: {}".format(len(Ydata),len(set(Ydata)),labels.getData()[:10]))
print("Coded Y code: {}".format(Ydata[:10]))

filepath='../data/addr/tmp1.txt'
testX, testY = load_data(filepath)

Xtestdata = vocab.encode(testX)
Ytestdata = labels.encode(testY)

#print(labels.word2idx.keys())
#print(set(testY))
#print(set(Ytestdata))

print("Coded Test X {} data: {}".format(len(Xtestdata),vocab.convData(testX)[:10]))
print("Coded Test X code: {}".format(Xtestdata[:10]))
print("Coded test Y size {} unique {} data: {}".format(len(Ytestdata),len(set(Ytestdata)),labels.convData(testY)[:10]))
print("Coded Y code: {}".format(Ytestdata[:10]))

no_classes = len(set(Ydata))
trainY = to_categorical(Ydata, nb_classes=no_classes)
#testY1 = to_categorical(Ytestdata, nb_classes=no_classes)

print("************",vocab.dict_size,len(vocab.vocab))

net = tflearn.input_data([None, 3])
net = tflearn.embedding(net, input_dim=vocab.dict_size, output_dim=50)
net = tflearn.fully_connected(net, 100, activation='tanh')
net = tflearn.dropout(net,0.5)
net = tflearn.fully_connected(net, no_classes, activation='softmax')
net = tflearn.regression(net, optimizer='adam', learning_rate=0.001, loss='categorical_crossentropy')

# Define model
model = tflearn.DNN(net)
# Start training (apply gradient descent algorithm)
model.fit( Xdata, trainY, n_epoch=40, validation_set=0.1, batch_size=64, show_metric=True)

# Predict surviving chances (class 1 results)
model.save('ner_model.tfl')
#pred = model.predict([Xtestdata, testY1])
pred = model.predict(Xtestdata)


with open('predict.tfl','wb') as f1:
  pickle.dump(pred,f1)

res = Result(Xtestdata,Ytestdata,pred,vocab,labels)

print("testX Rate:", pred[0][1])
print("testY Rate:", pred[1][1])

