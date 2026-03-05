# writers.py

def format_poly(coeffs):
    """Formats a tuple of coefficients into a readable polynomial string."""
    deg = len(coeffs) - 1
    terms = []
    for i, c in enumerate(coeffs):
        if c == 0 and deg - i != 0: continue
        power = deg - i
        term = f"{c}" if c != 1 or power == 0 else ""
        if term == "" and c == 1 and power > 0: term = "1"
        if power == 1: term += "x"
        elif power > 1: term += f"x^{power}"
        terms.append(term)
    
    terms = [t if t != "1x" else "x" for t in terms]
    terms = [t if not t.startswith("1x^") else t[1:] for t in terms]
    return " + ".join(terms) if terms else "0"

def polynomial_writer(queue, filename, poly_type):
    """
    A dedicated process that reads polynomials from a queue 
    and writes them to a file.
    """
    # We use a set to deduplicate, as multiple workers might 
    # find the same reducible polynomial via different factors.
    seen = set()
    count = 0
    
    print(f"[{poly_type.upper()} WRITER] Started. Writing to {filename}...")
    
    with open(filename, 'w') as f:
        f.write(f"--- {poly_type.upper()} POLYNOMIALS ---\n")
        
        while True:
            item = queue.get()
            
            # Check for the sentinel value to shut down the thread
            if item == "DONE":
                break
                
            if item not in seen:
                seen.add(item)
                f.write(format_poly(item) + "\n")
                count += 1

    print(f"[{poly_type.upper()} WRITER] Finished. Wrote {count} unique polynomials.")
