import math
import matplotlib
import scipy

# Parametros estimados
n = 60
p = 0.73
x_values = range(60)
probabilidade_de_x = []

def calculate_probability(x):
    return (math.factorial(n) / (math.factorial(x) * math.factorial(n - x))) * (p**x) * ((1 - p)**(n-x))

def sum(start, end, probabilities):
    accumulated_value = 0
    range_to_ve_summed = range(start, end)
    for x in range_to_ve_summed:
        accumulated_value += probabilities[x]
    return accumulated_value

for x in x_values:
    print(x)
    probabilidade_de_x.append(calculate_probability(x))

print(sum(40, 60, probabilidade_de_x))
print(sum(0, 40, probabilidade_de_x))
print(sum(0, 60, probabilidade_de_x))
