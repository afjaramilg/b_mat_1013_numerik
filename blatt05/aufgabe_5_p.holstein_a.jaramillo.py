# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: hydrogen
#       format_version: '1.3'
#       jupytext_version: 1.17.3
#   kernelspec:
#     display_name: numerik_kernel
#     language: python
#     name: numerik_kernel
# ---

# %%
# how can we represent a polynomial? the numpy Polynomial module and class
from numpy.polynomial import Polynomial

# %% [markdown]
# Rekursive Berechnung des interpolations Polynoms

# %%
def compute_interploation_polynom(points: list[tuple[float, float]]) -> Polynomial:
    # (x - x_k) * p_k+1,..,k+m - (x-x_k+m) * p_k,..,k+m-1 / (x_k+m - x_k)
    # it would be possible to create a cache so that we save the computed polynomial for a given inputs
    # so it would be more practical to calculate the polynomial if we add point
    if (len(points) == 1):
        return Polynomial([points[0][1]])
    else:
        polynomial_left_side = compute_interploation_polynom(points[1:])
        polynomial_right_side = compute_interploation_polynom(points[:-1])
        return (Polynomial([-points[0][0], 1]) * polynomial_left_side - Polynomial([-points[-1][0], 1]) * polynomial_right_side) / (points[-1][0] - points[0][0])
# %% [markdown]
# Inputs

# %%
# interpoltion polynomial with four points
four_points: list[tuple[float, float]] = [(55.7,1048.), (59.3,1111.), (62.6,1196.), (65.6,1354.)]

interpolation_polynomial_four_points: Polynomial = compute_interploation_polynom(four_points)

print(interpolation_polynomial_four_points)
# %%
# interpoltion polynomial with five points
five_points: list[tuple[float, float]] = [(55.7,1048.), (59.3,1111.), (62.6,1196.), (65.6,1354.), (57.7, 1080)]

interpolation_polynomial_five_points: Polynomial = compute_interploation_polynom(five_points)

print(interpolation_polynomial_five_points)
# %%
print(interpolation_polynomial_four_points(61.7))
# %%
print(interpolation_polynomial_five_points(61.7))
# %%

# %%

