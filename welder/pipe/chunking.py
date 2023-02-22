from welder.node import Pipe
import math

class SlidingWindowSplit(Pipe):
    
    def __init__(self, label: str, stride=150, chunk_size=200) -> None:
        super().__init__(label, inputs=[str], outputs=[list])
        self.stride = stride
        self.chunk_size = chunk_size

    def pipe(self):
        text_block = self.values[0]

        total_char = len(text_block)

        s = 0
        e = s + self.chunk_size

        do_for = math.ceil((total_char - self.chunk_size) / self.stride)

        chunks = []
        for i in range(do_for):
            s = s + self.stride
            e = e + self.stride if i != do_for else total_char
            
            chunks.append(text_block[s: e])

        return [chunks]
