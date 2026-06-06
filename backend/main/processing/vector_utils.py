from typing import List

import numpy as np
from numpy.linalg import norm

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        a_vec = np.array(a)
        b_vec = np.array(b)
        return float(np.dot(a_vec, b_vec) / (norm(a_vec) * norm(b_vec)))

def normalize_vector(v: object) -> np.ndarray:
        if isinstance(v, np.ndarray):
            return v.astype(float)

        if isinstance(v, list):
            return np.array(v, dtype=float)

        if isinstance(v, str):
            v = v.strip("[]")
            return np.array([float(x) for x in v.split(",")], dtype=float)

        raise TypeError(f"Unsupported vector type: {type(v)}")

def compute_centroid(vectors: List[List[float]]) -> List[float]:
    """
    Compute the centroid (mean vector) of a list of embedding vectors.
    Returns a Python list of floats.
    """

    if not vectors:
        return []

    # Convert to numpy array for efficient vector math
    arr = np.array(vectors, dtype=float)

    # Mean across rows → centroid
    centroid = np.mean(arr, axis=0)

    # Convert back to list for JSON‑compatibility
    return centroid.tolist()