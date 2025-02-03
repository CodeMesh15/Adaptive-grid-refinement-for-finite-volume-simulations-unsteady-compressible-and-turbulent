def compute_tecq(grad_p, hess_p):
    """Compute TECq criterion from gradients and Hessians."""
    delta_q1 = np.linalg.norm(grad_p, axis=1)
    delta_q2 = 0.5 * np.trace(hess_p, axis1=1, axis2=2)
    tecq = delta_q1 + delta_q2
    return tecq / np.max(tecq)  # Normalize
