import pulp
import math

flatten = lambda l: [item for sublist in l for item in sublist]


def get_room_and_visit(variable_name):
  split_var = variable_name.split('_')
  return 'Room-' + split_var[1] + ', Visits: ' + split_var[2]

target_visit = 30
total_visits_per_room = 11
total_rooms = 4

room_visit = pulp.LpProblem('Room Visit', pulp.LpMaximize)

life_portion_per_visit = [
  [round(math.log(v * (0.42 / i) + 1), 3) for v in range(total_visits_per_room)]
  for i in range(1, 5)
  ]

sos_variables = [
  [pulp.LpVariable('x_' + str(i) + '_' + str(j), cat='Binary') for j in range(total_visits_per_room)]
  for i in range(1, total_rooms + 1)
  ]

visits = [range(total_visits_per_room) for i in range(total_rooms)]

objective = flatten(
  [[sos_variables[i][j] * life_portion_per_visit[i][j] for j in range(total_visits_per_room)]
   for i in range(total_rooms)]
)

room_visit += pulp.lpSum(objective), 'Revenue'

for i in range(total_rooms):
  room_visit += pulp.lpSum(
    [sos_variables[i][j] for j in range(total_visits_per_room)]
  ) == 1, 'SOS constraint ' + str(i)

target_visit_constraint = flatten(
  [[sos_variables[i][j] * visits[i][j] for j in range(total_visits_per_room)]
   for i in range(total_rooms)]
)

# Subtracting the zero visits
room_visit += pulp.lpSum(target_visit_constraint) <= target_visit, 'Target visit constraint'

solved = room_visit.solve()

if solved == 1:
  for variable in room_visit.variables():
    if variable.varValue == 1:
      print get_room_and_visit(variable.name)

  print "Objective: {}".format(pulp.value(room_visit.objective))

