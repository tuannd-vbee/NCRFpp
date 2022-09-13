from main import evaluate, load_model_decode
from model.seqlabel import SeqLabel
from utils.data import Data
import torch

from utils.functions import read_instance_text 

# MODEL_DIR = 'saved_model'

data = Data()

data.dset_dir = 'saved_model/lstmcrf.dset'
data.load(data.dset_dir)

data.status = 'decode'
data.nbest = 1
data.load_model_dir = 'saved_model/lstmcrf.10.model'
data.HP_gpu = torch.cuda.is_available()

data.fix_alphabet()

model = SeqLabel(data)
model.load_state_dict(torch.load(data.load_model_dir))

def predict(text):
    tokens = text.split()
    lines = []
    for token in tokens:
        lines.append(token + ' - O')
    data.raw_texts, data.raw_Ids = read_instance_text(lines, data.word_alphabet, data.char_alphabet, data.feature_alphabets, data.label_alphabet, data.number_normalized, data.MAX_SENTENCE_LENGTH, data.sentence_classification, data.split_token)

    speed, acc, p, r, f, pred_results, pred_scores = evaluate(data, model, 'raw', data.nbest)
    
    # print('decode results:', len(pred_results))
    return pred_results[0]

print(predict('bốn bốn trăm ngàn'))
