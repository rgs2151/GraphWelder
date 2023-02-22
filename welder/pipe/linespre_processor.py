from welder.node import Pipe
import re

'''
Remove unwanted characters
Detect multiple sentence and split
Length threshold
Lower
Remove stop words
Wrap sentence with start and end token
'''

class LineParser(Pipe):

    def __init__(self, label: str, join_with=None) -> None:
        super().__init__(label, inputs=[list], outputs=[list])
        self.join_with = join_with
        if self.join_with: self.outs = [str]

    def join(self, results):
        return self.join_with.join(results)

class RemoveUnwantedChars(LineParser):
    # unwanted_chars = ['\n', '\t', '\r', '\xa0', '©', '\|', '™', r'[ ]{2,}', r'[a-z][\.]+[a-z]\. ']
    unwanted_chars = ['\n', '\t', '\r', '\xa0', '©', '\|', '™', r'[ ]{2,}', r'[a-zA-Z][\.]+[a-zA-Z]\.']
    # unwanted_chars = ['\n', '\t', '\r', '\xa0', '©', '\|', '™', r'[ ]{2,}', r'([a-z]+[\.][a-z]+)(\.)']

    def __init__(self, label: str, unwanted_chars=None, join_with=None) -> None:
        super().__init__(label, join_with=join_with)

        if unwanted_chars: self.unwanted_chars = unwanted_chars


    def pipe(self):
        remove = '|'.join(self.unwanted_chars)
        new_line = []
        for line in self.values[0]:
            line = re.sub(remove, '', line)
            new_line.append(line.strip())

        if self.join_with: new_line = self.join(new_line)
        return [new_line]


class RemoveSentenceEnders(LineParser):

    def __init__(self, label: str, join_with=None) -> None:
        super().__init__(label, join_with=join_with)

    def pipe(self):
        new_line = []
        for line in self.values[0]: pass


class Lower(LineParser):

    def __init__(self, label: str, join_with=None) -> None:
        super().__init__(label, join_with=join_with)

    def pipe(self):
        new_line = []
        for line in self.values[0]:
            line = line.lower()
            new_line.append(line.strip())

        if self.join_with: new_line = self.join(new_line)
        return [new_line]


class WordThreshold(LineParser):
    def __init__(self, label: str, thresh=3, join_with=None) -> None:
        super().__init__(label, join_with=join_with)
        self.thresh = thresh

    def pipe(self):
        new_line = []
        for line in self.values[0]:
            if len(line.split(' ')) > self.thresh:
                new_line.append(line.strip())

        if self.join_with: new_line = self.join(new_line)
        return [new_line]

class RemoveSpaces(LineParser):
    
    def __init__(self, label: str, join_with=None) -> None:
        super().__init__(label, join_with=join_with)

    def pipe(self):
        new_line = []
        for line in self.values[0]:
                if line: new_line.append(' '.join([c for c in line.split(' ') if c]).strip())

        if self.join_with: new_line = self.join(new_line)
        return [new_line]

class SplitIntoSentences(LineParser):
    sentence_enders = ['\. ', '\? ', '! ']
    def __init__(self, label: str, sentence_enders: list = None, join_with=None) -> None:
        super().__init__(label, join_with=join_with)

        if sentence_enders: self.sentence_enders = sentence_enders

    def pipe(self):
        new_line = []
        for line in self.values[0]:
            new_line.extend(re.split('|'.join(self.sentence_enders), line))
            
        
        if self.join_with: new_line = self.join(new_line)
        return [new_line]
