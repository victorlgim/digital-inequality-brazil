import numpy as np

def lorenz_curve(values: np.ndarray):
    """
    Returns normalized Lorenz Curve coordinates (x, y).
    """
    x = np.asarray(values).flatten()
    x = x[~np.isnan(x)]
    
    if len(x) == 0:
        return np.array([]), np.array([])
    
    x_sorted = np.sort(x)
    cum_values = np.cumsum(x_sorted)
    total = cum_values[-1]
    
    lorenz_x = np.linspace(0, 1, len(x_sorted) + 1)
    lorenz_y = np.insert(cum_values / total, 0, 0)
    
    return lorenz_x, lorenz_y
