import numpy as np

def gini(values: np.ndarray) -> float:
    """
    Computes the Gini coefficient for a 1D array.
    Efficient implementation commonly used in statistical literature.
    """

    x = np.asarray(values).flatten()
    
    x = x[~np.isnan(x)]
    
    if len(x) == 0:
        return np.nan
    
    x_sorted = np.sort(x)
    n = len(x_sorted)
    
    index = np.arange(1, n + 1)
    g = (np.sum((2 * index - n - 1) * x_sorted)) / (n * np.sum(x_sorted))
    
    return g
