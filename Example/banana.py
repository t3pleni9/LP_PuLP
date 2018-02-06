import pulp
import math

flatten = lambda l: [item for sublist in l for item in sublist]

def banana_price(base, discount, n):
  if n == 0:
    return 0
  if n == 1:
    return base
  current_price = banana_price(base, discount, n-1)
  return  current_price - discount * current_price

def get_number_of_bananas_from_vendor(variable_name):
  split_var = variable_name.split('_')
  return 'Vendor:' + split_var[1] + ', Bananas: ' + split_var[2]

banana_money = 28
total_bananas_per_vendor = 10
total_vendors = 3
vendor_schema = [{'base': 9, 'discount': 0.08}, {'base': 7, 'discount': 0.04}, {'base': 8, 'discount': 0.07}]


banana_shopping = pulp.LpProblem('Banana Shopping', pulp.LpMaximize)

banana_price = [
  [round(banana_price(scheme['base'], scheme['discount'], b), 2) for b in range(total_bananas_per_vendor + 1)]
  for scheme in vendor_schema
  ]

bananas = [range(total_bananas_per_vendor + 1) for i in range(total_vendors)]
selected_bananas = [
  [pulp.LpVariable('vendor_' + str(i) + '_' + str(j) + '_bananas', cat='Binary')
  for j in range(total_bananas_per_vendor + 1)]
  for i in range(1, total_vendors + 1)
  ]

for i in range(total_vendors):
  banana_shopping += pulp.lpSum(
    [selected_bananas[i][j] for j in range(total_bananas_per_vendor + 1)]
  ) == 1, 'SOS constraint ' + str(i)

total_bananas = flatten(
  [[selected_bananas[i][j] * bananas[i][j] for j in range(total_bananas_per_vendor + 1)]
   for i in range(total_vendors)]
)

banana_shopping += pulp.lpSum(total_bananas) <= total_vendors * total_bananas_per_vendor, 'Total available bananas'

target_banana_money = flatten(
  [[selected_bananas[i][j] * banana_price[i][j] * bananas[i][j] for j in range(total_bananas_per_vendor + 1)]
   for i in range(total_vendors)]
)

banana_shopping += pulp.lpSum(target_banana_money) <= banana_money, 'Available Banana Money'


banana_shopping += pulp.lpSum(total_bananas), 'Objective'

solved = banana_shopping.solve()

if solved == 1:
  for variable in banana_shopping.variables():
    if variable.varValue == 1:
      print get_number_of_bananas_from_vendor(variable.name)

  print "Objective: {}".format(pulp.value(banana_shopping.objective))
