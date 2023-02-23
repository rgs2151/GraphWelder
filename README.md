# 🧑‍🏭 GraphWelder: High-Performance MLOps Framework For Open Source Research

GraphWelder: High-Performance MLOps Framework For Open Source Research


# languagewelder PipeLine

**welder PipeLine module** is designed to represent each and every step in the project as `Pipe` to a `PipeLine`. `PipeLine` is an implementation of asyclic `Graph` with n `InputPipe` and `OutputPipe`.

## Quick Start

Let's create a pipe that accepts a `str` input and lowers it.

```python
from welder.node import Pipe

class LowerStr(Pipe):
	def __init__(self, label: str) -> None:
        super().__init__(label, inputs=[str], outputs=[str])

	def pipe(self):
		text = self.values[0]
		text = text.lower()
		return [text]
```

Each `Pipe` has to initialize `inputs` and `outputs` specifing the type of parameters to accept.
Each `Pipe` **Child** class has to implement a `pipe` method with **NO arguments!**.
Inputs to the `Pipe` are expected in the `self.values` instance variable with index equal to the index specified in the `inputs`.
Return to `pipe` method should correspond to `outputs` set to the `Pipe` class.

In order to use this functionality in `PipeLine` we need to specify `InputPipe` and `OutputPipe`.

```python
from welder.node import InputPipe, OutputPipe

Input1 = InputPipe('Input 1', inputs=[str], fix_inputs=1)
Pipe1 = LowerStr('Lower Text')
Output1 = OutputPipe('Output 1', outputs=[str])

PL = PipeLine()
PL.register(Input1, Pipe1)
PL.register(Pipe1, Output1)

results = PL.flow(['THIS is a TeXt'])
# results = 'this is a text'
```

## In More Detail...

* [class PipeLine](./README-PipeLine.md)
* [class Pipe](README-Pipe.md)
* [Pipe Documentation](pipe/README.md)

## Things Remaining...

* [ ] Checking `PipeLine` with multipl `OutputPipe` objects.
* [ ] Documentation for individual pipe functionalities.
* [ ] Missing `sequential_connect` usecase in the quick start.
* [ ] Adding `Pipe` uniqueness check in the `PipeLine` logs.
* [X] Adding `branch_connect` functionality to `PipeLine`.
* [ ] documentation for installing requirements and dependencies.

# Pipe Functionalities

Documentation for `Pipe` functionalities defined here...

Plese add your functionalities and documentation references here...

## Index

* htmlparser
* linepreprocessor
* chunking
* db


## Pipe

```python
class Pipe(Node):

    def __init__(self, label:str, inputs=[], outputs=[], fix_inputs=None) -> None:
        super().__init__(label, inputs=inputs, outputs=outputs, check_input=True, check_output=True, fix_inputs=fix_inputs)
        self.values = None
```

It is an extension of `Node` class. This class forms the base class to all the defined functionalities of the `PipeLine`. Each `Pipe` is represented by a unique `label`. Along with `Node` functionalities it contains a default implementation of the `pipe` method.

Each functionality for the `PipeLine` requires implementation of `pipe` method along with `inputs` and `outputs` defination of the `Node` object.

**`Pipe` Object is specificaly designed to work with the `PipeLine`. any change in its implementation can result in major breaking changes.**

| Property         | Functionality                                                                   |
| ---------------- | ------------------------------------------------------------------------------- |
| `values: list` | values set by the `set_inputs` method. Should be in sync with the `inputs`. |

| Method                                 | Functionality                                                                                                                                                             |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pipe() -> List[Any]`:               | Method should return the result for the functionality defined for the `PipeLine`.<br />Method takes no arguments and raises `NotImplementedError` if not overwritten. |
| `set_inputs(values: list) -> None:`  | Used by `PipeLine` to set inputs to the `Pipe` object.                                                                                                                |
| `set_outputs(values: list) -> None:` | pass                                                                                                                                                                      |

## Node

```python
class Node:
    inputs: list
    outputs: list
    total_inputs: int
    total_outputs: int
    check_input: bool
    check_output: bool

    label: str

```

Parent to all `Pipe` class representing the functionality to be executed.

All functionalities should contain `inputs: list` with types of accepted inputs and `outputs: list` with type of accepted outputs. These are used for compatiblity checking while connecting two `Node` objects and for type assertions.

Type assertion status are maintained by `check_inputs` and `check_outputs` flags. These flags can be used to determine type constraints. `(this flags were added to be used with PipeLine)`.

Each `Node` object is uniquely identified by the `label: str`. Label is used for representation and hashing purpose.

| Property                | Functionality                                                                                                                        |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `inputs: List[type]`  | Defines inputs to the `Node` Functionality.                                                                                        |
| `outputs: List[type]` | Defines outputs to the `Node` Functionality.                                                                                       |
| `total_inputs: int`   | Total number of inputs defined.                                                                                                      |
| `total_outputs: int`  | Total number of outputs defined.                                                                                                     |
| `check_input: bool`   | Flag specifying weather to assert inputs.                                                                                            |
| `check_output: bool`  | Flag specifying weather to assert outputs.                                                                                           |
| `label: str`          | Unique Identifier for the Node.<br />**Note: `__eq__` method for `Node` is set to `label` this might change in future.** |
| `ins: @Property`      | Setter and Getter for `inputs`.                                                                                                    |
| `outs: @Property`     | Setter and Getter for `outputs`.                                                                                                   |


## PipeLine

```python
class PipeLine(Graph):
    def __init__(self):
        super().__init__()
```

This class is a representation of the `Graph` object. It represents an acyclic graph. This class is modified to accept and initialize `Pipe` Inputs.

| Property                | Functionality                                               |
| ----------------------- | ----------------------------------------------------------- |
| `inputs: List[Pipe]`  | List of registered `InputPipe` objects to the `Graph.`  |
| `outouts: List[Pipe]` | List of registered `OutputPipe` objects to the `Graph`. |
| `logs: dict`          | Get a log of all the outputs generated during `flow`.     |

| Methods                                         | Functionality                                                                                                                    |
| :---------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------- |
| `register(pipe1: Node, pipe2: Node) -> None:` | Adds a directed edge between pipe1 and pipe2.                                                                                    |
| `flow(values: List): -> List:`                | Takes the corresponding `InputPipe` values and runs the `PipeLine` to generate the respective outputs at the `OutputPipe`. |
| `sequential_connect(pipes: List) -> Pipe:`    | Registeres a list of `Pipe` objects as sequence and returns the last connected `Pipe`.                                       |

| Exceptions            | For                                                                                                                                     |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `IncompatablePipes` | Occurs while registering two incompatible `Pipe`. Most likely occurs when `outputs` of `Pipe `does not match with the `inputs`. |

## Graph

```python
class Graph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.reverse_graph = defaultdict(list)
        self.V = 0
        self.all_nodes = []
```

Represents Graph object with topological sorting.

| Property                       | Functionality                                                    |
| ------------------------------ | ---------------------------------------------------------------- |
| `graph: defaultdict`         | Represents graph with `Node` and their directed edges.         |
| `reverse_graph: defaultdict` | Represents graph with `Node` and their reverse directed edges. |
| `V: int`                     | Number of vertices registered in the `Graph`.                  |
| `all_nodes: List[Pipe]`      | List of all registered `Node` object.                          |

| Property                                       | Functionality                                                  |
| ---------------------------------------------- | -------------------------------------------------------------- |
| `addEdge(node1: Node, node2: Node) -> None:` | Adds Directed edge between the `Node` objects.               |
| `topologicalSort() -> List[Node]:`           | Topologicaly sorts `Graph` using **Kahn's Algorithm**. |

| Error           | For                                      |
| --------------- | ---------------------------------------- |
| `CyclicGraph` | If cycles are detected in the `Graph`. |
