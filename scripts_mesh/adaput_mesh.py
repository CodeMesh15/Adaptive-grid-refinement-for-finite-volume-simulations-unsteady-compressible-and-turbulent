def automatic_period_control(prev_error, current_error):
    """Adjust adaptation interval using APC logic."""
    epsilon = (current_error - prev_error) / (current_error + prev_error)
    if epsilon <= 0:
        new_interval = max(10, int(adapt_interval * (1 - epsilon)))
    else:
        new_interval = max(10, int(adapt_interval * (1 - epsilon)))
    return new_interval
