

def convert_gbfs_to_dict(input_data, required_fields, optional_fields):
    """
    This function creates a dictionary for the SQLModel version of the object, formatting values as appropriate.
    required_fields and optional_fields represent required and optional fields as per GBFS spec.
    :param input_data: the input from the original GBFS file
    :param required_fields: a dict where the key is a field name in input_data
    and value is the function to apply to the associated value in input_data
    :param optional_fields: dict where the key is a field name in input_data
    and value is the function to apply to the associated value in input_data
    :return: a dictionary where each value associated to a key is in the correct format
    """
    res = {k: v(input_data[k]) for k, v in required_fields.items()}
    for k, v in optional_fields.items():
        if k in input_data:
            res[k] = v(input_data[k])
    return res
