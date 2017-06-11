import pulp

chocolate_factory = pulp.LpProblem("Chocolate Factory", pulp.LpMaximize)

x = pulp.LpVariable('x', lowBound=0, cat='Integer')
y = pulp.LpVariable('y', lowBound=0, cat='Integer')

chocolate_factory += 6 * x + 5 * y, "Profit"

chocolate_factory += x + y <= 5
chocolate_factory += 3 * x + 2 * y <= 12

chocolate_factory.solve()

for variable in chocolate_factory.variables():
  print "{} = {}".format(variable.name, variable.varValue)

print "Objective: {}".format(pulp.value(chocolate_factory.objective))
