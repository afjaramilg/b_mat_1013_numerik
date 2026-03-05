# main.py
import itertools
import math
import multiprocessing as mp
import numpy as np
from numba import njit
from writers import polynomial_writer  # Import our new writer module

# ==========================================
# C-Speed Math Engine
# ==========================================
@njit
def poly_mul_mod_numba(p1, p2, n):
    deg1, deg2 = len(p1) - 1, len(p2) - 1
    res = np.zeros(deg1 + deg2 + 1, dtype=np.int64)
    for i in range(len(p1)):
        for j in range(len(p2)):
            res[i+j] = (res[i+j] + p1[i] * p2[j]) % n
            
    start_idx = 0
    while start_idx < len(res) - 1 and res[start_idx] == 0:
        start_idx += 1
    return res[start_idx:]

def is_unit(poly, n):
    if len(poly) == 1 and math.gcd(poly[0], n) == 1:
        return True
    return False

# ==========================================
# Worker Process
# ==========================================
def _worker_process_factor(args):
    """Worker computes and instantly passes polynomials to the queue."""
    i, A, all_factors, n, target_degree, q_red = args
    local_reducible = set()
    
    if A == (0,) or is_unit(A, n):
        return local_reducible
        
    A_arr = np.array(A, dtype=np.int64)
    
    for B in all_factors[i:]:
        if B == (0,) or is_unit(B, n):
            continue
            
        B_arr = np.array(B, dtype=np.int64)
        P_arr = poly_mul_mod_numba(A_arr, B_arr, n)
        
        if len(P_arr) - 1 == target_degree:
            p_tuple = tuple(P_arr)
            # Only push to queue if we haven't seen it in THIS specific worker yet
            if p_tuple not in local_reducible:
                local_reducible.add(p_tuple)
                q_red.put(p_tuple) # Pass off to queue immediately
                
    # We still return the local set so the main thread can figure out the irreducibles later
    return local_reducible

# ==========================================
# Main Orchestrator
# ==========================================
def compute_ring_polynomials_fast(degree, n, q_red, q_irred):
    if degree < 1:
        raise ValueError("Degree must be at least 1.")

    all_factors = []
    for deg in range(degree + 1):
        if deg == 0:
            for c in range(n): all_factors.append((c,))
        else:
            for coeffs in itertools.product(range(1, n), *[range(n)]*deg):
                all_factors.append(coeffs)

    target_polys = set(itertools.product(range(1, n), *[range(n)]*degree))
    
    # Notice we append 'q_red' to the arguments sent to the workers
    pool_args = [(i, A, all_factors, n, degree, q_red) for i, A in enumerate(all_factors)]
    
    global_reducible = set()
    num_cores = max(1, mp.cpu_count() - 2) # Leave 2 cores free for our writer processes
    
    _ = poly_mul_mod_numba(np.array([1, 1], dtype=np.int64), np.array([1, 1], dtype=np.int64), n)
    
    print(f"--> Spawning pool with {num_cores} math cores...")
    
    with mp.Pool(processes=num_cores) as pool:
        for local_set in pool.imap_unordered(_worker_process_factor, pool_args):
            global_reducible.update(local_set)

    # Now that workers are done, we know which ones were NEVER generated
    irreducible_polys = target_polys - global_reducible
    
    print("--> Computation done. Pushing irreducibles to queue...")
    for p in irreducible_polys:
        q_irred.put(p)

# ==========================================
# Execution Entry Point
# ==========================================
if __name__ == "__main__":
    n_mod = 6  
    target_degree = 4
    
    # 1. Create a Manager to safely handle queues across process boundaries
    manager = mp.Manager()
    q_reducible = manager.Queue()
    q_irreducible = manager.Queue()
    
    # 2. Spin up the Writer Processes
    writer_red = mp.Process(target=polynomial_writer, args=(q_reducible, "reducible.txt", "reducible"))
    writer_irred = mp.Process(target=polynomial_writer, args=(q_irreducible, "irreducible.txt", "irreducible"))
    
    writer_red.start()
    writer_irred.start()
    
    # 3. Run the computation, passing the queues
    compute_ring_polynomials_fast(target_degree, n_mod, q_reducible, q_irreducible)
    
    # 4. Send the "DONE" signal to shut down the writers gracefully
    q_reducible.put("DONE")
    q_irreducible.put("DONE")
    
    # 5. Wait for the writers to finish flushing to disk
    writer_red.join()
    writer_irred.join()
    
    print("\nAll tasks completed successfully!")
