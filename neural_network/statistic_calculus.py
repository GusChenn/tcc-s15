from scipy.stats import binom
import matplotlib.pyplot as plt

# Approximated parameters
n = 60
p = 0.73
x_values = list(range(n + 1))

mean, var = binom.stats(n, p)

dist = [binom.pmf(x, n, p) for x in x_values]

print("x\tP(X = x)")
for i in range(n + 1):
    print(str(x_values[i]) + "\t" + str(dist[i]))

print("mean = " + str(mean))
print("variance = " + str(var))

plt.bar(x_values, dist)
plt.show()
