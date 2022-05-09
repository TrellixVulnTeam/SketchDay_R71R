import torch

import gluonnlp as nlp
import numpy as np
from tqdm import tqdm, tqdm_notebook

#kobert
from diary.ml_models.KoBert.kobert.utils import get_tokenizer
from diary.ml_models.KoBert.kobert.pytorch_kobert import get_pytorch_kobert_model
from diary.ml_models.bert_classifier import BERTClassifier

#transformers
import numpy as np
import gluonnlp as nlp
from torch.utils.data import Dataset

bertmodel, vocab = get_pytorch_kobert_model()
model = BERTClassifier(bertmodel, dr_rate=0.5)
model.load_state_dict(torch.load('diary/ml_models/real_model.pt', map_location=torch.device('cpu')))
model.eval()
tokenizer = get_tokenizer()
tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)

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
        pass
    def predict(self, input_data):
        max_len = 500
        batch_size = 32
        
        data = [input_data["data"], '0']
        dataset_another = [data]

        another_test = BERTDataset(dataset_another, 0, 1, tok, vocab, max_len, True, False)
        test_dataloader = torch.utils.data.DataLoader(another_test, batch_size=batch_size, num_workers=5)
        

        for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(test_dataloader):
            token_ids = token_ids.long()
            segment_ids = segment_ids.long()

            valid_length= valid_length
            label = label.long()

            out = model(token_ids, valid_length, segment_ids)

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
                    test_eval.append("평온")
                elif np.argmax(logits) == 4:
                    test_eval.append("행복")
                test_logit = [0]*5
                for i in range(len(test_logit)):
                    test_logit[i] = float((logits[i] - min(logits))/(max(logits) - min(logits)))
                print(logits)
                print(test_logit)
            print(">> 입력하신 내용에서 " + test_eval[0] + "이 느껴집니다.")
        return test_logit, test_eval[0]