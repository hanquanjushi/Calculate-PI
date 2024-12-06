import decimal
import time
import matplotlib.pyplot as plt

def pi():
    """
    Compute Pi to the current precision.

    Notes
    -----
    Taken from https://docs.python.org/3/library/decimal.html#recipes
    """
    decimal.getcontext().prec += 2  # extra digits for intermediate steps
    three = decimal.Decimal(3)      # substitute "three=3.0" for regular floats
    lasts, t, s, n, na, d, da = 0, three, 3, 1, 0, 0, 24
    while s != lasts:
        lasts = s
        n, na = n + na, na + 8
        d, da = d + da, da + 32
        t = (t * n) / d
        s += t
    decimal.getcontext().prec -= 2
    return +s  # unary plus applies the new precision

# Set up precisions and time recording
precisions = range(1000, 10001, 1000)  # 1000, 2000, ..., 10000
times = []

for precision in precisions:
    decimal.getcontext().prec = precision
    start_time = time.time()
    pi_value = pi()
    end_time = time.time()
    times.append(end_time - start_time)
    print(f"Precision: {precision}, Time taken: {end_time - start_time:.4f} seconds")

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(precisions, times, marker="o", linestyle="-", color="b")
plt.title("Time to Compute π at Different Precisions")
plt.xlabel("Precision (Number of Digits)")
plt.ylabel("Time Taken (seconds)")
plt.grid(True)
plt.show()