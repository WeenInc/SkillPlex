
def get_attribute_or_key(response_message, attribute_name):
    """
    Retrieve the value of an attribute or key from an object or dictionary.

    Args:
    response_message: The object or dictionary from which to retrieve the value.
    attribute_name (str): The name of the attribute or key.

    Returns:
    The value of the attribute or key, or None if not found.
    """
    if hasattr(response_message, attribute_name):
        return getattr(response_message, attribute_name)
    elif attribute_name in response_message:
        return response_message.get(attribute_name)
    else:
        return None