# Solving Discrete Space problems with PuLP

## Problem Statement:
### The Life Portion Rooms
    There are 4 rooms which contain Life portions. 
    The life portion obtained at each visit in each roo is governed by the formula:
`f_i(v) = log(v*(0.42/i) + 1)` where `i` is the room number, and `v` is the visit.
 
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

## Solution:
The above problem is an example of discrete optimization as the Problem set and solution set are in the discrete space, ie. Only discrete number of inputs and corresponding outputs are available.

#### Special Ordered Sets ([SOS](https://en.wikipedia.org/wiki/Special_ordered_set))
In discrete optimization, a special ordered set (SOS) is an ordered set of variables, used as an additional way to specify integrality conditions in an optimization model. Special order sets are basically a device or tool used in branch and bound methods for branching on sets of variables, rather than individual variables, as in ordinary mixed integer programming.

Special ordered sets are of two types:  
*SOS-1*: are a set of variables, at most one of which can take a strictly positive value, all others being at 0. They most frequently apply where a set of variables are actually 0-1 variables.  
*SOS-2*: an ordered set of non-negative variables, of which at most two can be non-zero, and if two are non-zero these must be consecutive in their ordering. Special Ordered Sets of type 2 are typically used to model non-linear functions of a variable in a linear model. 

Other sources: [LPSolve](http://lpsolve.sourceforge.net/5.5/SOS.htm)

### Modeling the problem statement:

In pure mathematical way the problem can be modeled as follows: 

`LifePortion(v) = Sum(f_i(v_i))`  
`Maximize LifePortion(v)`  
Where `v_i` is the total visit made to room `i` and `f_i(v) = log(v*(0.42/i) + 1)`  
Subject to constraints:  
`Sum(v_i) <= 30`  
`v -> R, 0 <= v <= 9`  
`i -> R, 1 <= i <= 4`
  
#### Converting the problem to SOS-1 problem.
`LifePortion(v) = Sum(x_ij * f_i(v_ij))`
`Maximize LifePortion(v)`
Where `v_ij` is the `j` visits made to room `i`  
Subject to constraints: 
`x_ij -> {0,1}`  
`Sum(x_ij*v_ij) <= 30`  
`Sum(x_i) = 1`  
`v -> R, 0 <= v <= 9`  
`j -> R, 0 <= v <= 9`  
`i -> R, 1 <= i <= 4`

This problem has now been converted to a linear programming problem in `x`  
The optimal visits per room would be obtained by looking at visits with `x_ij == 1` where `i` is the room number and `j` is the visit.

    