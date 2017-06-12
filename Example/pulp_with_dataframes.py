import pulp
import pandas as pd
import operator as op


class CatFoodProblem:
  def __init__(self, data, data_constraints):
    self.data = data
    self.constraints = data_constraints

    self.__equality_relations__ = {
      '==': op.eq,
      '<=': op.le,
      '<' : op.lt,
      '>=': op.ge,
      '>' : op.gt
    }

  def optimize(self):
    cat_food_model = pulp.LpProblem('The Cat food problem', pulp.LpMinimize)
    ingredient_vars = pulp.LpVariable.dicts('Ingr', self.data.Stuff, 0)
    cat_food_model += pulp.lpSum(
      [row.Cost * ingredient_vars[row.Stuff]
       for index, row in self.data.iterrows()
       ]), 'Total Cost of Ingredients per can'

    for index, constraint in self.constraints.iterrows():
      cat_food_model += self.__equality_relations__[constraint.equality_relation](
        self.__get_constraint_sum(constraint.column_name, ingredient_vars),
        constraint.constraint_value
      ), constraint.constraint_name

    solved = cat_food_model.solve()

    if solved == 1:
      data_variables = [(variable.name, variable.varValue) for variable in cat_food_model.variables()]
      return data_variables, pulp.value(cat_food_model.objective)

    raise 'Unable to solve'

  def __get_constraint_sum(self, column_name, ingredient_vars):
    if column_name == '-':
      return pulp.lpSum([ingredient_vars[row.Stuff] for index, row in self.data.iterrows()])

    return pulp.lpSum(
      [row[column_name] * ingredient_vars[row.Stuff] for index, row in self.data.iterrows()]
    )


cat_food_data = pd.read_csv('data/cat_food/cat_food_data.csv', delimiter=',')
constraints = pd.read_csv('data/cat_food/constraints.csv', delimiter=',')

cat_food_problem = CatFoodProblem(cat_food_data, constraints)

variables, objective = cat_food_problem.optimize()
print variables
print objective

