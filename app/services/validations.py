def check_valid_patch(request, valid_keys):
    if not set(request.keys()).issubset(valid_keys):
        raise KeyError({
            "valid_keys": valid_keys,
            "recieved_keys": list(request.keys())
        })