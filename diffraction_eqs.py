# Calculate intensity profile observed after diffraction of a coherent plane wave
# by a circular object. Create look-up table for this.

import numpy as np
from scipy.special import jn
import scipy.interpolate

# Per Eq. 11 in Rocques & Moncuquet 2000
def lommel_u(n, x, y):
    '''Lommel function U_n(x, y) for x <= y.

    Parameters:
    ----------
    n : int
        Order of the Lommel function.
    x : float
        First argument of the Lommel function. Must be less than or equal to y.
    y : float
        Second argument of the Lommel function.
    '''
    if x > y:
        raise ValueError("x must be less than or equal to y.")
    sum_result = 0
    for k in range(50):  # Summation to 50 terms should be accurate enough
        term = ((-1)**k * (x / y)**(n + 2 * k) * jn(n + 2 * k, np.pi * x * y))
        sum_result += term
    return sum_result

# Per Eqs. 9 and 10 in Rocques & Moncuquet 2000
def occultation_intensity(r, rho):
    '''Intensity profile for a TNO occultation at distance r from the shadow center.
    
    Parameters:
    ----------
    r : float
        Distance from the center of the shadow in Fresnel units.
    rho : float
        Radius of the TNO in Fresnel units.'''
    if r >= rho:
        # Outside the shadow (Equation 9)
        u1 = lommel_u(1, rho, r)
        u2 = lommel_u(2, rho, r)
        term1 = 1 + u1**2 + u2**2
        term2 = -2 * u1 * np.sin(np.pi / 2 * (r**2 + rho**2))
        term3 = 2 * u2 * np.cos(np.pi / 2 * (r**2 + rho**2))
        return term1 + term2 + term3
    else:
        # Inside the shadow (Equation 10)
        u0 = lommel_u(0, r, rho)
        u1 = lommel_u(1, r, rho)
        return u0**2 + u1**2
    
if __name__ == '__main__':
    import time
    import os
    import matplotlib.pyplot as plt
    
    # Create lookup table for the intensity profile.
    num_points = 400
    r_points = np.linspace(0, 20, num_points)
    rho_points = np.linspace(0.01, 20, num_points)
    lut_array = np.zeros((num_points ** 2, 3))
    for i, r in enumerate(r_points):
        for j, rho in enumerate(rho_points):
            lut_array[i * num_points + j] = [r, rho, occultation_intensity(r, rho)]

    # Save LUT to csv file
    directory = os.path.dirname(os.path.abspath(__file__))
    np.savetxt(directory + '/occultation_intensity_lut.csv', lut_array, delimiter=',', header='r,rho,intensity', comments='')

    # Create interpolator
    interpolator = scipy.interpolate.CloughTocher2DInterpolator(lut_array[:, :2], lut_array[:, 2])

    # See whether it's faster to interpolate from lookup table or calculate directl
    grid_x, grid_y = np.mgrid[0:10:100j, 0.01:10:100j]
    t0 = time.time()
    result1 = np.zeros((100, 100))
    for i in range(100):
        for j in range(100):
            result1[i, j] = occultation_intensity(grid_x[i, j], grid_y[i, j])
    t1 = time.time()
    result2 = interpolator((grid_x, grid_y))
    t2 = time.time()
    print("Direct calculation took", t1 - t0, "seconds.")
    print("Interpolation took", t2 - t1, "seconds.")
    
   # Check that the interpolated result is still accurate
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    ax[0].imshow(result1, extent=(0.01, 10, 0, 10), aspect='auto')
    ax[0].set_xlabel("r")
    ax[0].set_ylabel("rho")
    ax[0].set_title("Direct calculation")
    ax[1].imshow(result1, extent=(0.01, 10, 0, 10), aspect='auto')
    ax[1].set_xlabel("r")
    ax[1].set_ylabel("rho")
    ax[1].set_title("Interpolation")
    plt.show()