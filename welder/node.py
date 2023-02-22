class UtilsCheck:

    @staticmethod
    def check_if_list_contains_only_types(list_to_check): # check utility
        if not isinstance(list_to_check, list):
            raise ValueError('expected a list')

        if not all([isinstance(x, type) for x in list_to_check]):
            raise ValueError('list should contain only types')

class Node:

    def __init__(self, label: str) -> None: self.label = str(label)

    def __str__(self) -> str: return self.label

    def __repr__(self) -> str: return self.__str__()

    def __eq__(self, __o: object) -> bool: return self.__str__() == __o.__str__()

    def __hash__(self) -> int: return hash(self.__str__())


class PipeNode(Node):
    inputs: list
    outputs: list
    total_inputs: int
    total_outputs: int
    check_input: bool
    check_output: bool

    label: str

    def __init__(self, label: str, inputs=[], outputs=[], check_input=True, check_output=True, fix_inputs=None) -> None:
        super().__init__(label)
        self.ins = inputs
        self.outs = outputs
        self.check_input = check_input # Not type checked
        self.check_output = check_output

        if fix_inputs: self.__on_fix_inputs(fix_inputs)

    def set_check(self, param, value):
        if param=="out": self.check_output = value
        elif param=='in': self.check_input = value
        else: raise ValueError('No such parameter')

    @property
    def ins(self): return self.inputs
    
    @ins.setter
    def ins(self, ins: list):
        try:
            UtilsCheck.check_if_list_contains_only_types(ins)
        except ValueError as err:
            raise ValueError('inputs invalid')
        
        self.inputs = ins
        self.total_inputs = len(self.inputs)

    @property
    def outs(self): return self.outputs
    
    @outs.setter
    def outs(self, outs: list):
        try:
            UtilsCheck.check_if_list_contains_only_types(outs)
        except ValueError as err:
            raise ValueError('outputs invalid')
        
        self.outputs = outs
        self.total_outputs = len(self.outputs)

    # mandatory to node
    def __on_fix_inputs(self, fix_inputs: int):
        if self.total_inputs != fix_inputs: raise ValueError(f'fixed {fix_inputs} inputs, received {self.total_inputs}')


class Pipe(PipeNode):

    def __init__(self, label:str, inputs=[], outputs=[], fix_inputs=None) -> None:
        super().__init__(label, inputs=inputs, outputs=outputs, check_input=True, check_output=True, fix_inputs=fix_inputs)
        self.values = None


    def pipe(self):
        raise NotImplementedError('pipe method not implemented')


    def set_inputs(self, values):
        if len(values) != self.total_inputs:
            raise ValueError(f'Expected {self.total_inputs}, got {len(values)}')

        for v, t in zip(values, self.inputs):
            if not isinstance(v, t): raise ValueError(f'Expected {self.inputs} got {[type(x) for x in values]}')

        self.values = values

    def set_outputs(self, values):
        pass


class InputPipe(Pipe):

    def __init__(self, label: str, inputs=[], fix_inputs=None) -> None:
        super().__init__(label, inputs=inputs, outputs=inputs, fix_inputs=fix_inputs)

    def pipe(self):
        return self.values


class OutputPipe(Pipe):

    def __init__(self, label: str, outputs=[], check=True) -> None:
        super().__init__(label, inputs=[], outputs=outputs)
        self.set_check('in', False)
        self.set_check('out', check)

    def set_inputs(self, values):
        self.values = values

    def pipe(self): return [self.values]


class Join(Pipe):
    
    def __init__(self, label:str, inputs=[], outputs=[]) -> None:
        super().__init__(label, inputs=inputs, outputs=outputs, fix_inputs=None)

    def is_joinable(self): 
        '''
        Takes 2 Pipe Obj and checks if 2 outputs are mergable
        '''
        raise NotImplementedError('is_joinable not implemented')

    class JoinError(Exception): pass

    def set_inputs(self, values):
        self.values = values


class MergeJoin(Join):

    def __init__(self, label:str, inputs=[], outputs=[]) -> None:
        super().__init__(label, inputs=inputs, outputs=outputs)
        self.set_check('out', False)

    def pipe(self):
        input1 = self.values[0]
        input2 = self.values[1]

        def make_inputs(input1, input2, level=-1):
            add_to_this = []
            if isinstance(input1, list) and isinstance(input2, list):
                if len(input1) == 1 and len(input2) == 1 or level > 0:
                    add_to_this = input1[0]
                    add_to_this.extend(input2[0])
                
                else:
                    for val1, val2 in zip(input1, input2):
                        add_to_this.append(make_inputs(val1, val2, 1))

            elif isinstance(input2, list):
                add_to_this = input2
                add_to_this.append(input1)
            
            elif isinstance(input1, list):
                add_to_this = input1
                add_to_this.append(input2)

            else:
                add_to_this = [input1, input2]

            return add_to_this
        
        results = [make_inputs(input1, input2)]
        self.outputs = [type(x) for x in results]
        self.set_check('out', True)
        return results


    def is_joinable(self, pipe1: Pipe, pipe2: Pipe):
        if pipe1.outputs != pipe2.outputs:
            return False
        
        return True


class ConcatJoin(Join):

    def __init__(self, label: str, inputs=[], outputs=[]) -> None:
        super().__init__(label, inputs=inputs, outputs=outputs)
        self.set_check('out', False)
        self.set_check('in', False)

    def pipe(self):
        values1 = self.values[0]
        values2 = self.values[1]
        values1.extend(values2)
        return values1
    
    def is_joinable(self, pipe1: Pipe, pipe2: Pipe):
        return True