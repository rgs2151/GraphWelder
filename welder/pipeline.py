from collections import defaultdict
from typing import Sequence
from welder.graph import Graph
from welder.node import InputPipe, Join, Node, OutputPipe, Pipe

class PipeLine(Graph):

    def __init__(self):
        super().__init__()
        self.inputs = []
        self.outputs = []

    def register(self, pipe1: Node, pipe2: Node):
        if not isinstance(pipe1, Node) or not isinstance(pipe2, Node):
            raise ValueError('cannot register pipes, it should be of type Node')

        if pipe1.outputs != pipe2.inputs and pipe1.check_output and pipe2.check_input:
            raise PipeLine.IncompatablePipes(f'{pipe1} incompatible with {pipe2} expected {pipe1.outputs} got {pipe2.inputs}')

        if isinstance(pipe1, InputPipe) and pipe1 not in self.all_nodes: self.inputs.append(pipe1)
        if isinstance(pipe2, InputPipe): raise PipeLine.IncompatablePipes('InputPipe improperly connected')
        if isinstance(pipe2, OutputPipe) and pipe2 not in self.all_nodes: self.outputs.append(pipe2)

        self.addEdge(pipe1, pipe2)

    class IncompatablePipes(Exception): pass

    def __init_pipe(self, values):
        logs = defaultdict(None)
        if not self.inputs: raise ValueError('No InputPipe detected')

        if not self.outputs: raise ValueError('No OutPutPipe detected')

        if len(values) != len(self.inputs): raise ValueError(f'Expected inputs {len(self.inputs)} got {len(values)}')

        for input, val in zip(self.inputs, values):
            input: InputPipe
            input.set_inputs(val)
            logs[input] = input.pipe()

        self.logs = logs

    def flow(self, values):
        self.__init_pipe(values)

        load_order = self.topologicalSort()
        for pipe in load_order:
            pipe: Pipe
            values = []
            if isinstance(pipe, InputPipe): continue

            fetch = self.reverse_graph[pipe]
            for fetch_pipe in fetch:
                values.append(self.logs[fetch_pipe])

            if isinstance(pipe, Join): values = [values]

            if not values: values = [[]]

            # print('>>', values, pipe)
            pipe.set_inputs(*values)
            values = pipe.pipe()
            # print('<<', values)

            if not all([isinstance(x, y) for x, y in zip(values, pipe.outputs)]) and pipe.check_output:
                raise PipeLine.IncompatablePipes(f'{pipe} output validation failed expected outputs {pipe.outputs}')

            self.logs[pipe] = values

        results = []
        for output in self.outputs:
            output: OutputPipe
            results.append(self.logs[output])

        return results

    def sequential_connect(self, pipes: list) -> Pipe:
        for pipe in pipes:
            if not isinstance(pipe, Pipe): raise ValueError(f"{pipe} Invalid")

        if len(pipes) < 2: raise ValueError(f"cannot connect pipes sequentialy")

        previous = pipes[0]
        for pipe in pipes[1:]:
            self.register(previous, pipe)
            previous = pipe

        return previous

    def branch_connect(self, branches: list, join_pipe: Join):
        if not isinstance(branches, list): raise ValueError('branches should be of type list.')
        if len(branches) != 2: raise ValueError(f'Expected 2 branches received {len(branches)}')

        if not isinstance(join_pipe, Join): raise ValueError('join_pipe should be of type Join.')
        
        for branch in branches:
            self.register(self.sequential_connect(branch), join_pipe)

        return join_pipe