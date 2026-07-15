"""
Algorithm Complexity Comparison Demo
=====================================
Compare actual runtime of different algorithms solving the same task.
"""

import time
import random
import sys
import math

# Increase recursion limit
sys.setrecursionlimit(10000)

# ============================================================
# Helper functions
# ============================================================

def measure_time(func, *args, **kwargs):
    """Measure function execution time in seconds"""
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return result, elapsed

def print_result(name, size, elapsed, complexity_hint=""):
    """Unified output format"""
    hint = f"  <- {complexity_hint}" if complexity_hint else ""
    print(f"  {name:30s}  n={size:>8d}  {elapsed:>12.6f}s{hint}")

def sep(title):
    """Print section separator"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


# ============================================================
# Task 1: Search -- find target value in array
# ============================================================

def linear_search(arr, target):
    """Linear search O(n) -- iterate one by one"""
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1

def binary_search(arr, target):
    """Binary search O(log n) -- halve each step (requires sorted array)"""
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

def demo_search():
    sep("Task 1: Search -- find target value in array")

    sizes = [10_000, 100_000, 1_000_000, 10_000_000]

    for n in sizes:
        print(f"\n--- Data size n = {n:,} ---")
        arr = list(range(n))  # sorted array
        target = n - 1        # worst case: find the last element

        # Linear search O(n)
        _, t = measure_time(linear_search, arr, target)
        print_result("Linear Search O(n)", n, t, f"~{n} comparisons")

        # Binary search O(log n)
        _, t = measure_time(binary_search, arr, target)
        print_result("Binary Search O(log n)", n, t, f"~{int(math.log2(n))} comparisons")


# ============================================================
# Task 2: Sorting -- sort a random array
# ============================================================

def bubble_sort(arr):
    """Bubble sort O(n^2) -- adjacent swap"""
    a = arr.copy()
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a

def insertion_sort(arr):
    """Insertion sort O(n^2) -- insert into sorted portion"""
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

def quick_sort(arr):
    """Quick sort O(n log n) average -- divide & conquer + partition"""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)

def merge_sort(arr):
    """Merge sort O(n log n) -- divide & conquer merge"""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    # Merge
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def tim_sort(arr):
    """Timsort O(n log n) -- Python built-in, hybrid merge+insertion"""
    return sorted(arr)

def demo_sorting():
    sep("Task 2: Sorting -- sort a random array")

    sizes = [500, 1_000, 2_000, 5_000]

    for n in sizes:
        print(f"\n--- Data size n = {n:,} ---")
        arr = [random.randint(0, n * 10) for _ in range(n)]

        # O(n^2) algorithms -- only test at small sizes
        if n <= 2_000:
            _, t = measure_time(bubble_sort, arr)
            print_result("Bubble Sort O(n^2)", n, t, f"~{n**2:,} operations")
        else:
            print(f"  {'Bubble Sort O(n^2)':30s}  n={n:>8d}  {'(skipped, too slow)':>12s}  <-~{n**2:,} ops")

        if n <= 5_000:
            _, t = measure_time(insertion_sort, arr)
            print_result("Insertion Sort O(n^2)", n, t, f"~{n**2:,} operations")
        else:
            print(f"  {'Insertion Sort O(n^2)':30s}  n={n:>8d}  {'(skipped, too slow)':>12s}")

        # O(n log n) algorithms
        _, t = measure_time(quick_sort, arr)
        print_result("Quick Sort O(n log n)", n, t, f"~{int(n * math.log2(n)):,} operations")

        _, t = measure_time(merge_sort, arr)
        print_result("Merge Sort O(n log n)", n, t, f"~{int(n * math.log2(n)):,} operations")

        _, t = measure_time(tim_sort, arr)
        print_result("Timsort O(n log n) built-in", n, t, "C implementation, very fast")


# ============================================================
# Task 3: Fibonacci numbers
# ============================================================

def fib_recursive(n):
    """Recursive O(2^n) -- exponential explosion"""
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)

def fib_memo(n, memo=None):
    """Memoized recursion O(n) -- avoid recomputation"""
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n not in memo:
        memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

def fib_dp(n):
    """Dynamic programming O(n) -- bottom-up"""
    if n <= 1:
        return n
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr

def fib_matrix(n):
    """Matrix fast exponentiation O(log n) -- using [[1,1],[1,0]]"""
    if n <= 1:
        return n
    def mat_mul(a, b):
        return [
            a[0]*b[0] + a[1]*b[2],
            a[0]*b[1] + a[1]*b[3],
            a[2]*b[0] + a[3]*b[2],
            a[2]*b[1] + a[3]*b[3],
        ]
    def mat_pow(m, p):
        # Identity matrix
        result = [1, 0, 0, 1]
        while p:
            if p & 1:
                result = mat_mul(result, m)
            m = mat_mul(m, m)
            p >>= 1
        return result
    base = [1, 1, 1, 0]
    return mat_pow(base, n - 1)[0]

def demo_fibonacci():
    sep("Task 3: Fibonacci Numbers F(n)")

    # Recursion can only handle small n
    print("\n--- Small n: observe exponential vs linear difference ---")
    for n in [10, 15, 20, 25, 30, 35]:
        print(f"\n  n = {n}:")

        if n <= 35:
            _, t = measure_time(fib_recursive, n)
            print_result("  Recursive O(2^n)", n, t, f"~{2**n:,} calls")
        else:
            print(f"  {'Recursive O(2^n)':30s}  n={n:>8d}  {'(skipped)':>12s}")

        _, t = measure_time(fib_memo, n)
        print_result("  Memoized O(n)", n, t, f"~{n} calculations")

        _, t = measure_time(fib_dp, n)
        print_result("  DP O(n)", n, t, f"~{n} iterations")

        _, t = measure_time(fib_matrix, n)
        print_result("  Matrix Pow O(log n)", n, t, f"~{int(math.log2(n))} steps")

    # Large n: compare fast algorithms
    print("\n--- Large n: O(log n) advantage becomes clear ---")
    for n in [1000, 10_000, 100_000, 1_000_000]:
        print(f"\n  n = {n:,}:")

        _, t = measure_time(fib_dp, n)
        print_result("  DP O(n)", n, t)

        _, t = measure_time(fib_matrix, n)
        print_result("  Matrix Pow O(log n)", n, t)

        # Memoization may hit recursion depth limit at large n
        if n <= 1_000:
            _, t = measure_time(fib_memo, n)
            print_result("  Memoized O(n)", n, t)
        else:
            print(f"  {'Memoized O(n)':30s}  n={n:>8d}  {'(stack risk, skip)':>12s}")


# ============================================================
# Task 4: Find duplicate element
# ============================================================

def find_duplicate_nested(arr):
    """Nested loops O(n^2) -- compare every pair"""
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] == arr[j]:
                return arr[i]
    return None

def find_duplicate_sort_first(arr):
    """Sort then scan O(n log n) -- sort first, then find adjacent duplicates"""
    a = sorted(arr)
    for i in range(len(a) - 1):
        if a[i] == a[i + 1]:
            return a[i]
    return None

def find_duplicate_set(arr):
    """Hash set O(n) -- one pass with set lookup"""
    seen = set()
    for val in arr:
        if val in seen:
            return val
        seen.add(val)
    return None

def demo_duplicate():
    sep("Task 4: Find duplicate element in array")

    sizes = [500, 1_000, 2_000, 5_000, 10_000]

    for n in sizes:
        print(f"\n--- Data size n = {n:,} ---")
        # Construct: first n-1 unique, last one is a duplicate (worst case)
        arr = list(range(n - 1)) + [n - 2]

        # O(n^2) -- skip if too slow
        if n <= 2_000:
            _, t = measure_time(find_duplicate_nested, arr)
            print_result("Nested Loops O(n^2)", n, t, f"~{n*(n-1)//2:,} comparisons")
        else:
            print(f"  {'Nested Loops O(n^2)':30s}  n={n:>8d}  {'(skipped, too slow)':>12s}  <-~{n*(n-1)//2:,} comparisons")

        # O(n log n)
        _, t = measure_time(find_duplicate_sort_first, arr)
        print_result("Sort+Scan O(n log n)", n, t)

        # O(n)
        _, t = measure_time(find_duplicate_set, arr)
        print_result("Hash Set O(n)", n, t)


# ============================================================
# Task 5: Maximum subarray sum (Kadane vs Brute-force vs Divide & Conquer)
# ============================================================

def max_subarray_bruteforce(arr):
    """Brute-force O(n^2) -- enumerate all subarrays"""
    max_sum = float('-inf')
    for i in range(len(arr)):
        current_sum = 0
        for j in range(i, len(arr)):
            current_sum += arr[j]
            if current_sum > max_sum:
                max_sum = current_sum
    return max_sum

def max_subarray_kadane(arr):
    """Kadane's algorithm O(n) -- one-pass DP"""
    max_ending_here = max_so_far = arr[0]
    for x in arr[1:]:
        max_ending_here = max(x, max_ending_here + x)
        max_so_far = max(max_so_far, max_ending_here)
    return max_so_far

def max_subarray_divide_conquer(arr):
    """Divide & Conquer O(n log n) -- max subarray in left/right/cross"""
    def helper(lo, hi):
        if lo == hi:
            return arr[lo]
        mid = (lo + hi) // 2
        left_max = helper(lo, mid)
        right_max = helper(mid + 1, hi)

        # Max subarray crossing midpoint
        cross_left = float('-inf')
        s = 0
        for i in range(mid, lo - 1, -1):
            s += arr[i]
            cross_left = max(cross_left, s)

        cross_right = float('-inf')
        s = 0
        for i in range(mid + 1, hi + 1):
            s += arr[i]
            cross_right = max(cross_right, s)

        return max(left_max, right_max, cross_left + cross_right)

    return helper(0, len(arr) - 1)

def demo_max_subarray():
    sep("Task 5: Maximum Subarray Sum (Kadane vs Brute-force vs D&C)")

    sizes = [100, 200, 500, 1_000, 2_000]

    for n in sizes:
        print(f"\n--- Data size n = {n:,} ---")
        arr = [random.randint(-100, 100) for _ in range(n)]

        # O(n^2) -- skip if too slow
        if n <= 1_000:
            _, t = measure_time(max_subarray_bruteforce, arr)
            print_result("Brute-force O(n^2)", n, t, f"~{n*(n+1)//2:,} subarrays")
        else:
            print(f"  {'Brute-force O(n^2)':30s}  n={n:>8d}  {'(skipped, too slow)':>12s}  <-~{n*(n+1)//2:,} subarrays")

        # O(n log n)
        _, t = measure_time(max_subarray_divide_conquer, arr)
        print_result("Divide & Conquer O(n log n)", n, t)

        # O(n)
        _, t = measure_time(max_subarray_kadane, arr)
        print_result("Kadane O(n)", n, t)


# ============================================================
# Summary
# ============================================================

def show_summary():
    sep("Summary: Time Complexity Cheat Sheet")
    print("""
  Complexity      n=10         n=100        n=1,000      n=10,000      n=100,000     n=1,000,000
  ------------------------------------------------------------------------------------------------
  O(1)           1            1            1            1             1             1
  O(log n)       3            7            10           13            17            20
  O(n)           10           100          1,000        10,000        100,000       1,000,000
  O(n log n)     33           664          9,966        132,877       1,660,964     19,931,569
  O(n^2)         100          10,000       1,000,000    100,000,000   10^10         10^12
  O(2^n)         1,024        1.3x10^30    inf          inf           inf           inf
  O(n!)          3,628,800    ~10^158      inf          inf           inf           inf

  Key Takeaways:
  * O(log n)   -- barely grows with input size, e.g. binary search
  * O(n)       -- linear growth, e.g. single pass traversal
  * O(n log n) -- slightly above linear, optimal sorting lower bound
  * O(n^2)     -- quadratic growth, becomes painful at n=10^4
  * O(2^n)     -- exponential explosion, infeasible beyond n~30
    """)


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    print("+" + "="*70 + "+")
    print("|" + " "*15 + "Algorithm Time Complexity Comparison Demo" + " "*15 + "|")
    print("|" + " "*10 + "Same Task, Different Algorithms, Vast Difference" + " "*10 + "|")
    print("+" + "="*70 + "+")

    demo_search()
    demo_sorting()
    demo_fibonacci()
    demo_duplicate()
    demo_max_subarray()
    show_summary()

    print("\nDone.")
