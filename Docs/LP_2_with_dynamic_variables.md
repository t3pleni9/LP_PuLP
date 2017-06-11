# Linear programming with Python:  
Code example: pulp_with_dataframes.py  
In the previous example, it was shown how to solve a basic Linear programming problem.  
This section deals with solving a linear programming problem where the number of variables are determined at the runtime. The source of data would be a DB, http request, or a csv file. For this section a CSV file would be used.

## Problem statement:
    Whiskas cat food, is manufactured by Uncle Ben’s. 
    Uncle Ben’s want to produce their cat food products as cheaply as possible while ensuring they meet the stated nutritional analysis requirements shown on the cans. 
    Thus they want to vary the quantities of each ingredient used while still meeting their nutritional standards.
### Data:

|Stuff           |Protein   |Fat   |Fibre  |Salt | Cost($)| 
|:---------------|---------:|-----:|------:|----:|-------:|             
|Secret Stuff 1  |      0.10|  0.08|  0.001|0.002|   0.013|
|Secret Stuff 2  |      0.20|  0.10|  0.005|0.005|   0.008|
|Secret Stuff 3  |      0.15|  0.11|  0.003|0.007|   0.010|
|Secret Stuff 4  |      0.00|  0.01|  0.100|0.002|   0.002|
|Secret Stuff 5  |      0.04|  0.01|  0.150|0.008|   0.005|
|         Gel    |      0.00|  0.00|  0.000|0.000|   0.001|
        

[Blending Problem](https://pythonhosted.org/PuLP/CaseStudies/a_blending_problem.html#problem-description) gives a good discription at using dictionaries to store the data and create constraints and objective functions.

In this example DataFrames would be used to store data and create constraint and objective functions.

`$> import pandas as pd`  
`$> data = pd.read_csv('data/cat_food/cat_food_data.csv', delimiter=',')`  

### Lp model
This problem is a cost reduction problem. Thus the model needs to be minimized for cost.  
`$> cat_food_model = pulp.LpProblem("The Cat food problem", pulp.LpMinimize)`

### Lp Variables:
[LpVariable.dicts](https://www.coin-or.org/PuLP/pulp.html?highlight=lpvariable.dicts#pulp.LpVariable.dicts)
    
    LpVariable.dicts(name, indexs, lowBound=None, upBound=None, cat=0, indexStart=[])
    Creates a dictionary of LP variables
    
    This function creates a dictionary of LP Variables with the specified
    associated parameters.
    Parameters:	
    name – The prefix to the name of each LP variable created
    indexs – A list of strings of the keys to the dictionary of LP variables, and the main part of the variable name itself
    lowbound – The lower bound on these variables’ range. Default is negative infinity
    upBound – The upper bound on these variables’ range. Default is positive infinity
    cat – The category these variables are in, Integer or Continuous(default)
    Returns:	
    A dictionary of LP Variables

`$> variables = data.Stuff`  
`$> ingredient_vars = pulp.LpVariable.dicts("Ingr", variables, 0)`  
`$> ingredient_vars`

    {
        'Secret Stuff 1': Ingr_Secret_Stuff_1, 
        'Secret Stuff 2': Ingr_Secret_Stuff_2, 
        'Secret Stuff 3': Ingr_Secret_Stuff_3, 
        'Secret Stuff 4': Ingr_Secret_Stuff_4, 
        'Secret Stuff 5': Ingr_Secret_Stuff_5, 
                'Gel' : Ingr_Gel
    }

### Objective function:
The objective function would be to deduce a relation between all the ingredients and the cost of production. The DataFrame columns and list comprehension can be used to generate the objective function.

[pulp.lpSum](https://pythonhosted.org/PuLP/pulp.html?highlight=lpsum#pulp.lpSum) function is used to obtain the variable vector.

`$> cat_food_model += pulp.lpSum([row.Cost * ingredient_vars[row.Stuff] for index, row in data.iterrows()]), "Total Cost of Ingredients per can"`

### Constraints:

Constraints for the given problem are also supplied as a CSV file.

|constraint_name   |constraint_value|column_name|equality_relation|
|:-----------------|---------------:|:----------|----------------:|
|PercentagesSum    |             100|-          |               ==|
|ProteinRequirement|             8.0|Protein    |              \>=|
|FatRequirement    |             6.0|Fat        |              \>=|
|FibreRequirement  |             2.0|Fibre      |               <=|
|SaltRequirement   |             0.4|Salt       |               <=|

`$> constraints = pd.read_csv('data/cat_food/constraints.csv', delimiter=',')`

This example uses a hash map which maps the string equality constraints with their respective functions

`$> import operator as op`  
`$> equality_relations = {`  
`...  '==': op.eq,`  
`...  '<=': op.le,`  
`...  '<' : op.lt,`  
`...  '>=': op.ge,`  
`...  '>' : op.gt`  
`...}`

The vector relationship is build using `pulp.lpSum` function. The hash map is used to apply the equality constructs between the vector and constrain value.

`for index, constraint in constraints.iterrows():`  
`...   cat_food_model += equality_relations[constraint.equality_relation](`  
`...     get_constraint_sum(constraint.column_name, ingredient_vars),`  
`...     constraint.constraint_value`  
`...   ), constraint.constraint_name`

`get_constraint_sum` returns the lpSum vector for each constraint type from the original data.

`$> pulp.lpSum([row[column_name] * ingredient_vars[row.Stuff] for index, row in data.iterrows()])`

### Solution
`$> cat_food_model.solve()`

The final result obtained is 
    
    [
        ('Ingr_Secret_Stuff_2', 60.0), 
        ('Ingr_Secret_Stuff_1', 0.0), 
        ('Ingr_Gel', 40.0), 
        ('Ingr_Secret_Stuff_3', 0.0), 
        ('Ingr_Secret_Stuff_4', 0.0), 
        ('Ingr_Secret_Stuff_5', 0.0)
    ]
