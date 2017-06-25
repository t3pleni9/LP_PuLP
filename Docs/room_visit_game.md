# Solving Discrete Space problems with PuLP

## Problem Statement:
### The Life Portion Rooms
    There are 4 rooms which contain Life portions. 
    The life portion obtained at each visit is governed by the formula:
`LifePortion(v) = log(v*(0.42/i) + 1)` where `i` is the room number, and `v` is the visit.
 
    Each room can be visited a maximum of 10 times. 
    There is a maximum 30 visits which can be made in total.
    The aim is to collect the maximum amount of life portion in the 30 visits.

## Problem break down

#### Data:
|Room No/Visit  |0    |1    |2    |3    |4    |5    |6    |7    |8    |9    |
|:--------------|----:|----:|----:|----:|----:|----:|----:|----:|----:|----:|
|1              |0.000|0.351|0.610|0.815|0.986|1.131|1.258|1.371|1.472|1.564|
|2              |0.000|0.191|0.351|0.489|0.610|0.718|0.815|0.904|0.986|1.061|
|3              |0.000|0.131|0.247|0.351|0.445|0.531|0.610|0.683|0.751|0.815|
|4              |0.000|0.100|0.191|0.274|0.351|0.422|0.489|0.551|0.610|0.665|

The above data is non linear in nature, but discrete.

### Solution:
Non linear programming can be solved using the Lagrange multiplier method. This problem also can be converted to a linear programming problem, as the problem and solution space is discrete. The above problem is converted into a piece-wise linear function which then can be solved using the PuLP solver.
