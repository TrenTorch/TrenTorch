def same_object(var1_value, var2_value) -> bool:
    return id(var1_value) == id(var2_value)
