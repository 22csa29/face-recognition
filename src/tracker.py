from sort_tracker.sort import Sort

def create_tracker(tracker_type, model_weights, device, half):
    if tracker_type == 'sort':
        return Sort()
    else:
        raise ValueError(f"Unsupported tracker type: {tracker_type}")
