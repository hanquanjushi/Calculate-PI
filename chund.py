# Computed π to 1000000 digits in 38.26 seconds.
import math
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

def pi_chudnovsky_bs(digits):
    """
    Compute int(pi * 10**digits)

    This is done using Chudnovsky's series with binary splitting
    """
    C = 640320
    C3_OVER_24 = C**3 // 24

    def bs(a, b):
        """
        Computes the terms for binary splitting the Chudnovsky infinite series

        a(a) = +/- (13591409 + 545140134*a)
        p(a) = (6*a-5)*(2*a-1)*(6*a-1)
        b(a) = 1
        q(a) = a*a*a*C3_OVER_24

        returns P(a,b), Q(a,b) and T(a,b)
        """
        if b - a == 1:
            # Directly compute P(a,a+1), Q(a,a+1) and T(a,a+1)
            if a == 0:
                Pab = Qab = 1
            else:
                Pab = (6*a-5)*(2*a-1)*(6*a-1)
                Qab = a*a*a*C3_OVER_24
            Tab = Pab * (13591409 + 545140134*a) # a(a) * p(a)
            if a & 1:
                Tab = -Tab
        else:
            # Recursively compute P(a,b), Q(a,b) and T(a,b)
            # m is the midpoint of a and b
            m = (a + b) // 2
            # Recursively calculate P(a,m), Q(a,m) and T(a,m)
            Pam, Qam, Tam = bs(a, m)
            # Recursively calculate P(m,b), Q(m,b) and T(m,b)
            Pmb, Qmb, Tmb = bs(m, b)
            # Now combine
            Pab = Pam * Pmb
            Qab = Qam * Qmb
            Tab = Qmb * Tam + Pam * Tmb
        return Pab, Qab, Tab

    # how many terms to compute
    DIGITS_PER_TERM = math.log10(C3_OVER_24/6/2/6)
    N = int(digits/DIGITS_PER_TERM + 1)
    # Calclate P(0,N) and Q(0,N)
    P, Q, T = bs(0, N)
    one = 10**digits
    sqrtC = sqrt(10005*one, one)
    return (Q*426880*sqrtC) // T


def sqrt(n, one):
    """
    Return the square root of n as a fixed point number with the one
    passed in.  It uses a second order Newton-Raphson convergence.  This
    doubles the number of significant figures on each iteration.
    """
    # Use floating point arithmetic to make an initial guess
    floating_point_precision = 10**16
    n_float = float((n * floating_point_precision) // one) / floating_point_precision
    x = (int(floating_point_precision * math.sqrt(n_float)) * one) // floating_point_precision
    n_one = n * one
    while 1:
        x_old = x
        x = (x + n_one // x) // 2
        if x == x_old:
            break
    return x


if __name__ == "__main__":
    # List of digit counts to compute (1000, 2000, ..., 10000)
    digit_counts = list(range(1000, 10001, 1000))
    times = []

    # Calculate and time for each digit count
    for digits in digit_counts:
        start_time = time.time()
        pi_value = pi_chudnovsky_bs(digits)
        elapsed_time = time.time() - start_time
        times.append(elapsed_time)
        print(f"Computed π to {digits} digits in {elapsed_time:.2f} seconds.")

        if digits == 1000:
            # Print the first 1000 digits as a string
            pi_str = str(pi_value)[:digits]
            print(f"First 1000 digits of π: {pi_str}")

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(digit_counts, times, marker="o")
    plt.title("Execution Time for Computing Digits of π (Chudnovsky Algorithm)")
    plt.xlabel("Number of Digits")
    plt.ylabel("Time (seconds)")

    # Set x-axis to scientific notation
    plt.gca().xaxis.set_major_formatter(mticker.ScalarFormatter(useMathText=True))
    plt.gca().xaxis.set_major_locator(mticker.FixedLocator(digit_counts))
    plt.ticklabel_format(style="sci", axis="x", scilimits=(0, 0))

    plt.grid(True)
    plt.show()