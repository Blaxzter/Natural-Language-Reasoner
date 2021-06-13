def create_new_object(referenced_object, list_of_new_objects):
    for i in range(10000):
        new_object = f'{referenced_object}_{i}'
        if new_object not in list_of_new_objects:
            list_of_new_objects.append(new_object)
            return new_object
    raise Exception("We dont have any new objects left... sorry.")
