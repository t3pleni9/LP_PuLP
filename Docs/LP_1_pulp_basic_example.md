# Linear programming with Python: 
Code example: basic_example_1.py
## Basic example: [Introductory guide on linear programming](https://www.analyticsvidhya.com/blog/2017/02/lintroductory-guide-on-linear-programming-explained-in-simple-english/)

## Problem statement: 
	Consider a chocolate manufacturing company which produces only two types of chocolate – A and B.  
	Both the chocolates require Milk and Choco only.  To manufacture each unit of A and B, following quantities are required:

	Each unit of A requires 1 unit of Milk and 3 units of Choco
	Each unit of B requires 1 unit of Milk and 2 units of Choco
	The company kitchen has a total of 5 units of Milk and 12 units of Choco. On each sale, the company makes a profit of

	6 Currency per unit A sold
	5 Currency per unit B sold.
	Now, the company wishes to maximize its profit. How many units of A and B should it produce respectively?


## Objective function: The problem which is being optimized

	Chocolate A -> 1 Milk 3 Choco
	Chocolate B -> 1 Milk 2 Choco

	Milk -> 5
	Choco -> 12


	Profit on selling one unit of A -> 6, on selling x units of A -> 6x
	Profit on selling one unit of B -> 5, on selling y units of B -> 5y

	Total Profit (z) on selling x units of A and y units of B -> z = 6x + 5y
		=> Maximizing profit -> maximize 6x + 5y.
		= maximize(z)

	So z becomes the objective function required to be maximized.

## Constraints: Things which decide the outcome of the objective function.

	The company wants to maximize the profit given the constraint that they have 5 units of milk and 12 unit of choco.
	one unit of A requires 1 unit of milk, x units of A -> x units of milk
	one unit of B requires 1 unit of milk, y units of B -> y units of milk

	total milk = 5 Units

	x + y <= 5

	Similarily for choco

	one unit of A requires 3 unit of choco, x units of A -> 3x units of choco
	one unit of B requires 2 unit of choco, y units of B -> 2y units of choco

	total choco = 12 Units

	3x + 2y <= 12

	Also the company can produce 0 or more units of A and 0 or more units of B

	x >= 0
	y >= 0

## Solving the above LP problem using python/PuLP

`$> import pulp`

### Defining LP problem

`$> chocolate_factory = pulp.LpProblem("Chocolate Factory", pulp.LpMaximize)`

[LpProblem](https://www.coin-or.org/PuLP/pulp.html#pulp.LpProblem):

		class pulp.LpProblem(name='NoName', sense=1)
		This function creates a new LP Problem with the specified associated parameters

		Parameters:	
			name – name of the problem used in the output .lp file
			sense – of the LP problem objective. Either LpMinimize (default) or LpMaximize.
		Returns:	
			An LP Problem

### Defining linear programming variables:

`$> x = pulp.LpVariable('x', lowBound=0, cat='Integer')`  
`$> y = pulp.LpVariable('y', lowBound=0, cat='Integer')`

[LpVariable](https://www.coin-or.org/PuLP/pulp.html#pulp.LpVariable):

		class pulp.LpVariable(name, lowBound=None, upBound=None, cat='Continuous', e=None)

		Parameters:	
			name – The name of the variable used in the output .lp file
			lowbound – The lower bound on this variable’s range. Default is negative infinity
			upBound – The upper bound on this variable’s range. Default is positive infinity
			cat – The category this variable is in, Integer, Binary or Continuous(default)
			e – Used for column based modelling: relates to the variable’s existence in the objective function and constraints

### Objective function

`$> chocolate_factory += 6 * x + 5 * y, "Z"`

### Constraints:

`$> chocolate_factory += x + y <= 5`  
`$> chocolate_factory += 3 * x + 2 * y <= 12`

### The constructed LP problem looks as follows

`$> chocolate_factory`

	Chocolate Factory:
	MAXIMIZE
	6*x + 5*y + 0
	SUBJECT TO
	_C1: x + y <= 5

	_C2: 3 x + 2 y <= 12

	VARIABLES
	0 <= x Integer
	0 <= y Integer

### Solving the LP problem:
[LP Solvers](https://www.coin-or.org/PuLP/solvers.html):  
	PuLP supports open source linear programming solvers such as CBC and GLPK, as well as commercial solvers such as Gurobi and IBM’s CPLEX.  
`$> chocolate_factory.solve()`

The optimization status of the LP problem can be checked using `pulp.LpStatus`  
`$> pulp.LpStatus[chocolate_factory.status]
'Optimal'`

Different available statuses: [Link](https://www.coin-or.org/PuLP/constants.html)

We can now view the Optimal values for chocolate factory problem:

`$> for variable in chocolate_factory.variables():`  
`... print "{} = {}".format(variable.name, variable.varValue)`

	x = 2.0
	y = 3.0

And to view the optimized value of the objective function:

`$> pulp.value(chocolate_factory.objective)`

	27.0

So,

The chocolate factory needs to produce 2 units of A chocolate and 3 unit of B chocolate to have the maximum profit and the maximum profit obtained is 27.0 Currency units.









