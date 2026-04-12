import numpy as np
import time
import statistics

Q = 3329
NOISE_BOUND = 2
ITERATIONS = 50
WARMUP_RUNS = 5

def generate_small_noise(size):
    return np.random.randint(-NOISE_BOUND, NOISE_BOUND + 1, size)


def keygen(N):
    A = np.random.randint(0, Q, (N, N))
    s = generate_small_noise(N)
    e = generate_small_noise(N)
    b = (A @ s + e) % Q
    return (A, b), s


def encrypt(public_key, message, N):
    A, b = public_key
    r = generate_small_noise(N)
    e1 = generate_small_noise(N)
    e2 = generate_small_noise(1)

    message_bit = message % 2

    u = (A.T @ r + e1) % Q
    v = (b @ r + e2 + message_bit * (Q // 2)) % Q

    return (u, v)


def decrypt(ciphertext, private_key):
    u, v = ciphertext
    s = private_key

    value = (v - (u @ s)) % Q
    return 1 if Q//4 < value < 3*Q//4 else 0



def single_run(N):
    public_key, private_key = keygen(N)
    message = np.random.randint(0, Q)

    ct = encrypt(public_key, message, N)
    decrypt(ct, private_key)


def benchmark(N, name):
    for _ in range(WARMUP_RUNS):
        single_run(N)

    times = []

    for _ in range(ITERATIONS):
        start = time.perf_counter()
        single_run(N)
        end = time.perf_counter()

        times.append((end - start) * 1000) 

    avg_time = statistics.mean(times)
    stdev_time = statistics.stdev(times)

    A = np.random.randint(0, Q, (N, N))
    memory_kb = A.nbytes / 1024

    return avg_time, stdev_time, memory_kb



def main():

    scenarios = {
        "Lightweight": 128,
        "Medium": 256,
        "High Security": 512
    }

    print("\n===== PQC IoT BENCHMARK (Professional) =====\n")
    print("{:<15} {:<10} {:<15} {:<15} {:<15}".format(
        "Scenario", "N", "Avg Time(ms)", "Std Dev", "Memory(KB)"
    ))
    print("-" * 75)

    for name, N in scenarios.items():
        avg, std, mem = benchmark(N, name)

        print("{:<15} {:<10} {:<15.4f} {:<15.4f} {:<15.2f}".format(
            name, N, avg, std, mem
        ))


if __name__ == "__main__":
    main()
