from welder.node import Pipe
from haystack.pipelines import GenerativeQAPipeline, ExtractiveQAPipeline


class QuestionsGenerative(Pipe):

    def __init__(self, label: str, questions, generator_top_k=5, retriever_top_k=10) -> None:
        '''
        Args: 
            label: label of the pipe
            questions: list of questions
            generator_top_k: number of answers to generate
            retriever_top_k: number of documents to retrieve
        '''

        super().__init__(label, inputs=[GenerativeQAPipeline])
        self.set_check('out', False)
        self.questions = questions
        self.generator_top_k = generator_top_k
        self.retriever_top_k = retriever_top_k

    def pipe(self):
        pipe = self.values[0]
        output = []
        for question in self.questions:
            result = pipe.run(query=question, params={
                "Generator": {"top_k": self.generator_top_k}, "Retriever": {"top_k": self.retriever_top_k}})
            output.append(result)

        return [output]


class QuestionsExtractive(Pipe):

    def __init__(self, label: str, questions, reader_top_k=5, retriever_top_k=10) -> None:
        super().__init__(label, inputs=[ExtractiveQAPipeline])
        self.set_check('out', False)
        self.questions = questions
        self.reader_top_k = reader_top_k
        self.retriever_top_k = retriever_top_k

    def pipe(self):
        pipe = self.values[0]
        output = []
        for question in self.questions:

            result = pipe.run(query=question, params={
                "Reader": {"top_k": self.reader_top_k}, "Retriever": {"top_k": self.retriever_top_k}})
            answer  = result
            output.append(result)
        return [output]