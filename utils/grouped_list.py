def grouper(input_list, list_size):
    grouped_list = list()
    index = list(range(0, len(input_list), list_size))
    for i in index:
        grouped_list.append(input_list[i:i + list_size])
    return grouped_list