import torch
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import gluonnlp as nlp
import numpy as np
from tqdm import tqdm, tqdm_notebook

#kobert
from kobert.utils import get_tokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model
from kobert_tokenizer import KoBERTTokenizer

#transformers
from transformers import AdamW
from transformers.optimization import get_cosine_schedule_with_warmup
import numpy as np
import gluonnlp as nlp
from torch.utils.data import Dataset, DataLoader

class BERTClassifier(nn.Module):
    def __init__(self,
                bert,
                hidden_size = 768,
                num_classes=5,   ##클래스 수 조정##
                dr_rate=None,
                params=None):
        super(BERTClassifier, self).__init__()
        self.bert = bert
        self.dr_rate = dr_rate

        self.classifier = nn.Linear(hidden_size , num_classes)
        if dr_rate:
            self.dropout = nn.Dropout(p=dr_rate)
    
    def gen_attention_mask(self, token_ids, valid_length):
        attention_mask = torch.zeros_like(token_ids)
        for i, v in enumerate(valid_length):
            attention_mask[i][:v] = 1
        return attention_mask.float()

    def forward(self, token_ids, valid_length, segment_ids):
        attention_mask = self.gen_attention_mask(token_ids, valid_length)
        
        _, pooler = self.bert(input_ids = token_ids, token_type_ids = segment_ids.long(), attention_mask = attention_mask.float().to(token_ids.device))
        if self.dr_rate:
            out = self.dropout(pooler)
        return self.classifier(out)

class BERTDataset(Dataset):
    def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer,vocab, max_len,
                pad, pair):

        transform = nlp.data.BERTSentenceTransform(
            bert_tokenizer, max_seq_length=max_len,vocab=vocab, pad=pad, pair=pair)
        
        self.sentences = [transform([i[sent_idx]]) for i in dataset]
        self.labels = [np.int32(i[label_idx]) for i in dataset]

    def __getitem__(self, i):
        return (self.sentences[i] + (self.labels[i], ))

    def __len__(self):
        return (len(self.labels))

class EmotionAnalysis:
    def __init__(self):
        cal_dev = 'cpu'
        self.device = torch.device(cal_dev) 
        bertmodel, vocab = get_pytorch_kobert_model()
        self.model = BERTClassifier(bertmodel,  dr_rate=0.5)
        self.model.load_state_dict(torch.load('diary/ml_models/real_model.pt', map_location=cal_dev))
        # self.model = torch.load('model1.pt')

    def predict(self, input_data):

        bertmodel, vocab = get_pytorch_kobert_model()

        max_len = 100
        batch_size = 32

        tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')
        tok=tokenizer.tokenize
    
        data = [input_data["data"], '0']
        dataset_another = [data]

        another_test = BERTDataset(dataset_another, 0, 1, tok, vocab, max_len, True, False)
        test_dataloader = torch.utils.data.DataLoader(another_test, batch_size=batch_size, num_workers=5)
        
        self.model.eval()

        for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(test_dataloader):
            token_ids = token_ids.long().to(self.device)
            segment_ids = segment_ids.long().to(self.device)

            valid_length= valid_length
            label = label.long().to(self.device)

            out = self.model(token_ids, valid_length, segment_ids)


            test_eval=[]
            for i in out:
                logits=i
                logits = logits.detach().cpu().numpy()

                if np.argmax(logits) == 0:
                    test_eval.append("불안")
                elif np.argmax(logits) == 1:
                    test_eval.append("분노")
                elif np.argmax(logits) == 2:
                    test_eval.append("슬픔")
                elif np.argmax(logits) == 3:
                    test_eval.append("중립")
                elif np.argmax(logits) == 4:
                    test_eval.append("행복")
            print(">> 입력하신 내용에서 " + test_eval[0] + "이 느껴집니다.")
        return ">> 입력하신 내용에서 " + test_eval[0] + "이 느껴집니다."