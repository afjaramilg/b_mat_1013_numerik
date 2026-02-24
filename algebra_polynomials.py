import itertools
import numpy.polynomial.polynomial as P

def evaluate_poly(poly, x, p):
    result = 0
    for i, coef in enumerate(poly):
        result = (result + coef * (x ** i)) % p
    return result

def has_root(poly, p):
    for a in range(p):
        if evaluate_poly(poly, a, p) == 0:
            return True
    return False

def divides(f, g, p):
    q, r = P.polydiv(f, g)
    r_int = [round(x) % p for x in r]
    return all(coef == 0 for coef in r_int)

def generate_monic_polynomials(degree, p):
    polys = []
    for coeffs in itertools.product(range(p), repeat=degree):
        poly = list(coeffs) + [1]
        polys.append(poly)
    return polys

def is_irreducible(poly, p):
    m = len(poly) - 1
    if m == 1:
        return True
    if has_root(poly, p):
        return False
    if m == 2 or m == 3:
        return True
    for d in range(2, m // 2 + 1):
        for g in generate_monic_polynomials(d, p):
            if divides(poly, g, p):
                return False
    return True

def main():
    n = int(input("Enter prime n: "))
    m = int(input("Enter degree m: "))

    polynomials = []
    for coeffs in itertools.product(range(n), repeat=m):
        poly = list(coeffs) + [1]
        polynomials.append(poly)

    irreducible_polys = []
    for poly in polynomials:
        if is_irreducible(poly, n):
            irreducible_polys.append(poly)

    print(f"Found {len(irreducible_polys)} monic irreducible polynomials over GF({n}) of degree {m}:")
    for poly in irreducible_polys:
        terms = []
        for i in range(len(poly)-1, -1, -1):
            coef = poly[i]
            if coef == 0:
                continue
            if i == 0:
                term = str(coef)
            elif i == 1:
                term = f"{coef}x" if coef != 1 else "x"
            else:
                term = f"{coef}x^{i}" if coef != 1 else f"x^{i}"
            terms.append(term)
        poly_str = " + ".join(terms)
        print(poly_str)

if __name__ == "__main__":
    main()
