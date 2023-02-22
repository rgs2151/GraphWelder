from transformers import AutoTokenizer, AutoModelForSequenceClassification
from haystack.nodes import DensePassageRetriever
from welder.node import Pipe
import torch
from tqdm import tqdm


class BertBoolQ(Pipe):
    '''
    A bert large uncased model trained on YES / NO questions.
    Imported from: lewtun/bert-large-uncased-wwm-finetuned-boolq
    '''
    def __init__(self, label: str) -> None:
        super().__init__(label, inputs=[DensePassageRetriever, list], outputs=[list])
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self.model_ckpt = "lewtun/bert-large-uncased-wwm-finetuned-boolq"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_ckpt)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_ckpt)

    def pipe(self):
        self.retriever = self.values[0]
        questions = self.values[1]
        results = []
        for question in tqdm(questions, desc = "Questions Asked"):
            answer = self.query(question)
            results.append(answer)
        return [results]

    def query(self, question: str):
        res = self.retriever.retrieve(query=question, top_k=10)
        contexts = ". ".join([doc.content for doc in res])

        if len(contexts) > 512: contexts = contexts[:512]

        inputs = self.tokenizer(question, contexts, return_tensors="pt")
        outputs = self.model.to(self.device)(**inputs.to(self.device))
        results = outputs[0][0].tolist()

        return ['no' if results[0] > results[1] else 'yes', results[1]]