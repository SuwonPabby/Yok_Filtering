import numpy as np
import re
import jamotools
from collections import Counter
np.random.seed(42)
import pickle
import keras
import pandas as pd
from lime import lime_text
from lime.lime_text import LimeTextExplainer
from pydub import AudioSegment
import pandas as pd
import os


class dataset():
  def __init__(self, dataset, train_dataset, max_fea = None, max_len = None):
    self.sentences = [sentence for sentence in dataset['text']]
    self.labels = [label for label in dataset['label']]
    self.korean = re.compile('[^1!ㄱ-ㅣ가-힣]+')
    self.vocab = self.get_vocab(max_fea)
    self.vocab_size = len(self.vocab)
    self.word2idx = {word : index for index, (word, count) in enumerate(self.vocab)}
    self.idx2word = {index : word for index, (word, count) in enumerate(self.vocab)}
    if max_len == None: 
      self.max_len = self.find_max_len()
    else : 
      self.max_len = max_len
    self.max_feature = max_fea

  def __getitem__(self, index):
    return (self.preprocess_sentence(self.sentences[index]), self.labels[index])

  def __len__(self):
    return len(self.labels)
  
  def get_vocab(self, max_fea):
    

    return train_dataset.get_vocab(max_fea)

  def jamo(self, sentences):
    result = []
    for sentence in sentences:
      chars = self.korean.sub('', jamotools.split_syllables(sentence))
      result.append(list(chars))
    
    return result

  def jamochar(self, char):
    char = self.korean.sub('', jamotools.split_syllables(char)) 
    return char

  def preprocess_sentence(self, sentence):
    result = []
    padding = '<PAD>'
    if len(sentence) > self.max_len:
      fixed_sen = ['<SOS>']
      fixed_sen += list(sentence[:self.max_len])
      fixed_sen += ['<EOS>']
    else:
      fixed_sen = ['<SOS>']
      fixed_sen += list(sentence) 
      fixed_sen += ['<EOS>']
      while len(fixed_sen) != self.max_len + 2: 
        fixed_sen += [padding] 
    
    for char in fixed_sen:
      if char in ['<SOS>', '<EOS>']:
        result.append(self.word2idx[char])
      elif char == '<PAD>':
        result+=([self.word2idx['<PAD>']] * 3)
      else:  
        sep_char = self.jamochar(char)
        if len(sep_char) == 2 : 
          result += ([self.word2idx[x] if x in self.word2idx.keys() else self.word2idx['<UNK>'] for x in sep_char]+[self.word2idx['<PAD>']])
        elif len(sep_char) == 1:
          result += ([self.word2idx[x] if x in self.word2idx.keys() else self.word2idx['<UNK>'] for x in sep_char]+([self.word2idx['<PAD>']]*2))
        elif sep_char == '.' or sep_char == ' ':
          result += ([self.word2idx['<PAD>']]*3)
        else : 
          result += [self.word2idx[x] if x in self.word2idx.keys() else self.word2idx['<UNK>'] for x in sep_char]
        
      
    self.padding(result)

    return result


  def padding(self, result):
    length = 3 * (self.max_len) + 2
    while len(result) < length :
      result.append(0)
                   

  


  def find_max_len(self):
    return max(len(item) for item in self.sentences)  


class dataset_train():
  def __init__(self, dataset, max_fea = None, max_len = None):
    self.sentences = [sentence for sentence in dataset['text']]
    self.labels = [label for label in dataset['label']]
    self.korean = re.compile('[^1!ㄱ-ㅣ가-힣]+')
    self.vocab = self.get_vocab(max_fea)
    self.vocab_size = len(self.vocab)
    self.word2idx = {word : index for index, (word, count) in enumerate(self.vocab)}
    self.idx2word = {index : word for index, (word, count) in enumerate(self.vocab)}
    if max_len == None: 
      self.max_len = self.find_max_len()
    else : 
      self.max_len = max_len
    self.max_feature = max_fea

  def __getitem__(self, index):
    return (self.preprocess_sentence(self.sentences[index]), self.labels[index])

  def __len__(self):
    return len(self.labels)
  
  def get_vocab(self, max_fea):
    initial_words = ['<EOS>', '<SOS>','<UNK>','<PAD>'] # 순서 반대로 들어감 ! Pad 가 index 0!
    counter = Counter()
    for char in self.jamo(self.sentences):
        counter.update(char)
  
    
    if max_fea == None:
      max_fea = len(counter.keys())

    vocab_words = counter.most_common(max_fea)

    for initial_word in initial_words:
      vocab_words.insert(0, (initial_word, 0))

    return vocab_words

  def jamo(self, sentences):
    result = []
    for sentence in sentences:
      chars = self.korean.sub('', jamotools.split_syllables(sentence))
      result.append(list(chars))
    
    return result

  def jamochar(self, char):
    char = self.korean.sub('', jamotools.split_syllables(char)) 
    return char

  def preprocess_sentence(self, sentence):
    result = []
    padding = '<PAD>'
    if len(sentence) > self.max_len:
      fixed_sen = ['<SOS>']
      fixed_sen += list(sentence[:self.max_len])
      fixed_sen += ['<EOS>']
    else:
      fixed_sen = ['<SOS>']
      fixed_sen += list(sentence) 
      fixed_sen += ['<EOS>']
      while len(fixed_sen) != self.max_len + 2: 
        fixed_sen += [padding] 
    
    for char in fixed_sen:
      if char in ['<SOS>', '<EOS>']:
        result.append(self.word2idx[char])
      elif char == '<PAD>':
        result+=([self.word2idx['<PAD>']] * 3)
      else:  
        sep_char = self.jamochar(char)
        if len(sep_char) == 2 : 
          result += ([self.word2idx[x] if x in self.word2idx.keys() else self.word2idx['<UNK>'] for x in sep_char]+[self.word2idx['<PAD>']])
        elif len(sep_char) == 1:
          result += ([self.word2idx[x] if x in self.word2idx.keys() else self.word2idx['<UNK>'] for x in sep_char]+([self.word2idx['<PAD>']]*2))
        elif sep_char == '.' or sep_char == ' ':
          result += ([self.word2idx['<PAD>']]*3)
        else : 
          result += [self.word2idx[x] if x in self.word2idx.keys() else self.word2idx['<UNK>'] for x in sep_char]
        
      
    self.padding(result)

    return result


  def padding(self, result):
    length = 3 * (self.max_len) + 2
    while len(result) < length :
      result.append(0)
                   

  


  def find_max_len(self):
    return max(len(item) for item in self.sentences)  



def yok_classifier_lime(sentence):
  
  print(train_dataset)
  sentence_dataframe= pd.DataFrame()   
  sentence_dataframe['text'] = sentence  
  sentence_dataframe['label'] = [1] * len(sentence)
  sentence_dataset = dataset(sentence_dataframe, train_dataset, max_fea = 5000, max_len = 10)
  input_data =np.zeros((len(sentence), 32))
  for i in range(32):
    for j in range(len(sentence)):
      input_data[j][i] = sentence_dataset[j][0][i]
  return np.array([[float(1-x), float(x)] for x in model_1.predict(input_data)])

def final_yok_classifing(sentence):
  class_names = ['욕설이 아님', '욕설']
  explainer = LimeTextExplainer(class_names=class_names)
  exp = explainer.explain_instance(sentence[0],yok_classifier_lime, num_features = 100)
  return exp.as_list()


import requests
import re
import json


class ClovaSpeechClient:
    # Clova Speech invoke URL
    invoke_url = 'https://clovaspeech-gw.ncloud.com/external/v1/1656/415473a357d9d696222e86407a96e6a0e022269c22dd2c8d5187a69c100f0097'
    # Clova Speech secret key
    secret = 'ba374fcca14d4ea7aed6e23911396516'

    def req_url(self, url, completion, callback=None, userdata=None, forbiddens=None, boostings=None, wordAlignment=True, fullText=True, diarization=None):
        request_body = {
            'url': url,
            'language': 'ko-KR',
            'completion': completion,
            'callback': callback,
            'userdata': userdata,
            'wordAlignment': wordAlignment,
            'fullText': fullText,
            'forbiddens': forbiddens,
            'boostings': boostings,
            'diarization': diarization,
        }
        headers = {
            'Accept': 'application/json;UTF-8',
            'Content-Type': 'application/json;UTF-8',
            'X-CLOVASPEECH-API-KEY': self.secret
        }
        return requests.post(headers=headers,
                             url=self.invoke_url + '/recognizer/url',
                             data=json.dumps(request_body).encode('UTF-8'))

    def req_object_storage(self, data_key, completion, callback=None, userdata=None, forbiddens=None, boostings=None,
                           wordAlignment=True, fullText=True, diarization=None):
        request_body = {
            'dataKey': data_key,
            'language': 'ko-KR',
            'completion': completion,
            'callback': callback,
            'userdata': userdata,
            'wordAlignment': wordAlignment,
            'fullText': fullText,
            'forbiddens': forbiddens,
            'boostings': boostings,
            'diarization': diarization,
        }
        headers = {
            'Accept': 'application/json;UTF-8',
            'Content-Type': 'application/json;UTF-8',
            'X-CLOVASPEECH-API-KEY': self.secret
        }
        return requests.post(headers=headers,
                             url=self.invoke_url + '/recognizer/object-storage',
                             data=json.dumps(request_body).encode('UTF-8'))

    def req_upload(self, file, completion, callback=None, userdata=None, forbiddens=None, boostings=None,
                   wordAlignment=True, fullText=True, diarization=None):
        request_body = {
            'language': 'ko-KR',
            'completion': completion,
            'callback': callback,
            'userdata': userdata,
            'wordAlignment': wordAlignment,
            'fullText': fullText,
            'forbiddens': forbiddens,
            'boostings': boostings,
            'diarization': diarization,
        }
        headers = {
            'Accept': 'application/json;UTF-8',
            'X-CLOVASPEECH-API-KEY': self.secret
        }
        print(json.dumps(request_body, ensure_ascii=False).encode('UTF-8'))
        files = {
            'media': open(file, 'rb'),
            'params': (None, json.dumps(request_body, ensure_ascii=False).encode('UTF-8'), 'application/json')
        }
        response = requests.post(headers=headers, url=self.invoke_url + '/recognizer/upload', files=files)
        return response


# res = ClovaSpeechClient().req_url(url='http://example.com/media.mp3', completion='sync')
# res = ClovaSpeechClient().req_object_storage(data_key='data/media.mp3', completion='sync')

def STT(file_dir):
    res = ClovaSpeechClient().req_upload(file= file_dir, completion='sync')
    result_ = res.text
    rw = re.compile('"words":')
    rt = re.compile(',"textEdited"')
    sw = re.compile(',"text":"')
    st = re.compile('","confidence"')
    iw = [m.end() for m in rw.finditer(result_)]
    it = [m.start() for m in rt.finditer(result_)]
    siw = [m.end() for m in sw.finditer(result_)]
    sit = [m.start() for m in st.finditer(result_)]

    stt_sentence = [result_[siw[i]:sit[i]] for i in range(len(siw))]
    del stt_sentence[-1]
    

    result = [result_[iw[i]:it[i]] for i in range(len(iw))]
    result = ",".join(result)
    result = result.replace('[','', -1)
    result = result.replace(']','', -1)
    result = result.replace('"','', -1)
    result = result.split(",")
    time_stemp = [[int(result[3*i]), int(result[3*i +1])] for i in range(len(result)//3)]
    stt_word = [result[3*i + 2] for i in range(len(result)//3)]


    return time_stemp, stt_word, stt_sentence


def get_swear(ts, stt, stt_sentence):
  res_sen =[]
  res_sen_temp=[]
  swear_ts = []
  split_number = 3
  for index, word in enumerate(stt):
    if index !=0 and index % split_number== 0:
      res_sen.append(res_sen_temp)
      res_sen_temp =[]
    if index == len(stt) -1:
      res_sen_temp.append(word)
      res_sen.append(res_sen_temp)
      break
    res_sen_temp.append(word)
  res_sen_str = []
  for i in range(len(res_sen)):
    res_sen_str.append(' '.join(res_sen[i]))
  lime_sen_result =[]
  lime_word_result = []
  for i in range(len(res_sen_str)):
    lime_sen_result.append(yok_classifier_lime([res_sen_str[i]]))
    lime_word_result.append(final_yok_classifing([res_sen_str[i]]))
  lime_word_result = sum(lime_word_result, [])
  lime_word_result_0 = [item[0] for item in lime_word_result]
  # print(lime_word_result)
  # print(lime_word_result_0)
  # print(lime_sen_result)
  
  for index, word in enumerate(stt):
    word = word.replace('.', '', -1)
    sen_res = lime_sen_result[index // split_number][0][1]
    if lime_word_result[lime_word_result_0.index(word)][1] > 0.9 - sen_res:
      swear_ts.append(ts[index])
      print(word)
  return swear_ts

  


def create_beep(duration):
    sps = 44100
    freq_hz = 1000.0
    vol = 0.1

    esm = np.arange(duration / 1000 * sps)
    wf = np.sin(2 * np.pi * esm * freq_hz / sps)
    wf_quiet = wf * vol
    wf_int = np.int16(wf_quiet * 32767)

    beep = AudioSegment(
        wf_int.tobytes(), 
        frame_rate=sps,
        sample_width=wf_int.dtype.itemsize, 
        channels=1
    )

    return beep



def using_beautiful_word(file_dir, format = 'mp3'):
  global ts, stt, stt_sen
  ts, stt, stt_sen= STT(file_dir)
  swear_ts = get_swear(ts, stt, stt_sen)
  sound = AudioSegment.from_mp3(file_dir)
  mixed_final = sound

  for i in range(len(swear_ts)):
     beep = create_beep(duration=swear_ts[i][1] - swear_ts[i][0])
     mixed_final = mixed_final.overlay(beep, position=swear_ts[i][0], gain_during_overlay=-50)

  return mixed_final

from moviepy.editor import * 
import os

def generate_output(video_dir, working_path):
  videoclip = VideoFileClip(video_dir)
  o_audio_dir = os.path.join(working_path + '/origin.mp3')
  n_audio_dir = os.path.join(working_path + '/new.mp3')
  videoclip.audio.write_audiofile(o_audio_dir)
  using_beautiful_word(o_audio_dir).export(n_audio_dir, format = "mp3")
  audioclip = AudioFileClip(n_audio_dir)

  videoclip.audio = audioclip
  return videoclip

from tensorflow.keras.optimizers import RMSprop
from keras import backend as K
def recall(y_target, y_pred):
    # clip(t, clip_value_min, clip_value_max) : clip_value_min~clip_value_max 이외 가장자리를 깎아 낸다
    # round : 반올림한다
    y_target_yn = K.round(K.clip(y_target, 0, 1)) # 실제값을 0(Negative) 또는 1(Positive)로 설정한다
    y_pred_yn = K.round(K.clip(y_pred, 0, 1)) # 예측값을 0(Negative) 또는 1(Positive)로 설정한다

    # True Positive는 실제 값과 예측 값이 모두 1(Positive)인 경우이다
    count_true_positive = K.sum(y_target_yn * y_pred_yn) 

    # (True Positive + False Negative) = 실제 값이 1(Positive) 전체
    count_true_positive_false_negative = K.sum(y_target_yn)

    # Recall =  (True Positive) / (True Positive + False Negative)
    # K.epsilon()는 'divide by zero error' 예방차원에서 작은 수를 더한다
    recall = count_true_positive / (count_true_positive_false_negative + K.epsilon())

    # return a single tensor value
    return recall


def precision(y_target, y_pred):
    # clip(t, clip_value_min, clip_value_max) : clip_value_min~clip_value_max 이외 가장자리를 깎아 낸다
    # round : 반올림한다
    y_pred_yn = K.round(K.clip(y_pred, 0, 1)) # 예측값을 0(Negative) 또는 1(Positive)로 설정한다
    y_target_yn = K.round(K.clip(y_target, 0, 1)) # 실제값을 0(Negative) 또는 1(Positive)로 설정한다

    # True Positive는 실제 값과 예측 값이 모두 1(Positive)인 경우이다
    count_true_positive = K.sum(y_target_yn * y_pred_yn) 

    # (True Positive + False Positive) = 예측 값이 1(Positive) 전체
    count_true_positive_false_positive = K.sum(y_pred_yn)

    # Precision = (True Positive) / (True Positive + False Positive)
    # K.epsilon()는 'divide by zero error' 예방차원에서 작은 수를 더한다
    precision = count_true_positive / (count_true_positive_false_positive + K.epsilon())

    # return a single tensor value
    return precision


def f1score(y_target, y_pred):
    _recall = recall(y_target, y_pred)
    _precision = precision(y_target, y_pred)
    # K.epsilon()는 'divide by zero error' 예방차원에서 작은 수를 더한다
    _f1score = ( 2 * _recall * _precision) / (_recall + _precision+ K.epsilon())
    
    # return a single tensor value
    
    return _f1score
def final_output(model_dir, video_dir, output_dir, working_path,train_dt):
  global model_1
  global train_dataset
  train_dataset = train_dt
  dependencies = {
    'precision': precision,
    'recall' : recall,
    'f1score' : f1score,
  }

  model_1 = keras.models.load_model(model_dir
                                      , custom_objects=dependencies)
  final_video_output = generate_output(video_dir, working_path)
  final_video_output.write_videofile(output_dir)

  
