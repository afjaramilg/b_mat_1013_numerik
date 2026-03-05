import galois
import itertools

def yield_polynomials(degree, field, poly_type="all"):
    """
    A memory-efficient generator that yields polynomials of a given degree 
    over a specified finite field.
    
    Args:
        degree (int): The degree of the polynomials.
        field (galois.FieldArray): The finite field (e.g., galois.GF(2)).
        poly_type (str): "all", "irreducible", or "reducible". 
                         Filters the output to save memory and processing time.
                         
    Yields:
        galois.Poly: The next polynomial matching the criteria.
    """
    if degree < 1:
        raise ValueError("Degree must be at least 1.")
        
    order = field.order
    leading_coeffs = range(1, order)
    other_coeffs = range(order)
    
    # Iterate through all valid coefficient combinations
    for coeffs in itertools.product(leading_coeffs, *[other_coeffs]*degree):
        poly = galois.Poly(coeffs, field=field)
        
        # Yield based on the requested type
        if poly_type == "all":
            # If "all", you might want to know if it's irreducible or not, 
            # so we yield a tuple: (polynomial, boolean_is_irreducible)
            yield (poly, poly.is_irreducible())
            
        elif poly_type == "irreducible" and poly.is_irreducible():
            yield poly
            
        elif poly_type == "reducible" and not poly.is_irreducible():
            yield poly

# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    # Define GF(5)
    GF5 = galois.GF(5)
    target_degree = 3
    
    print(f"Finding the first 5 IRREDUCIBLE polynomials of degree {target_degree} over GF({GF5.order}):")
    
    # Create the generator object
    irred_gen = yield_polynomials(target_degree, GF5, poly_type="irreducible")
    
    # We can use itertools.islice to grab just the first 5 without computing the rest
    for p in itertools.islice(irred_gen, 5):
        print(f"  {p}")
        
    print("\nProcessing ALL polynomials one-by-one (showing first 3):")
    all_gen = yield_polynomials(target_degree, GF5, poly_type="all")
    
    for i, (p, is_irred) in enumerate(all_gen):
        if i >= 3: 
            break
        status = "Irreducible" if is_irred else "Reducible"
        print(f"  {str(p):<20} -> {status}")
