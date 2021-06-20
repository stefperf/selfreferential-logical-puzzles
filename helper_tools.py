# miscellaneous utilities


def get_auto_labels(nr_possible_answers):
    """
    >>> get_auto_labels(3) == ['A', 'B', 'C']
    True
    """
    max_possible_answers = 26
    assert nr_possible_answers <= max_possible_answers
    return [chr(ord('A') + n) for n in range(nr_possible_answers)]


def list_text(elements, separator=', ', last_separator=' or '):
    """
    >>> list_text([1, 2, 3]) == '1, 2 or 3'
    True

    >>> list_text([1, 2, 3], '; ', '; and ') == '1; 2; and 3'
    True
    """
    text = separator.join([str(el) for el in elements])
    last_separator_index = text.rfind(separator)
    return text[:last_separator_index] + last_separator + text[last_separator_index + len(separator):]


DIRECTIONS = (+1, -1)


def index_in_list(element, element_list, direction=+1, not_found=-1):
    """
    >>> index_in_list('e', 'agreement', direction=+1)
    3

    >>> index_in_list('e', 'agreement', direction=-1)
    6

    >>> index_in_list('x', 'agreement')
    -1
    """
    if direction == +1:
        list_to_search = element_list
        index_offset = 0
    elif direction == -1:
        list_to_search = element_list[::-1]
        index_offset = len(element_list) - 1
    else:
        raise ValueError(f'Direction "{direction}" is neither of the accepted directions '
                         f'+1 (:= forwards) and -1 (:= backwards')
    try:
        return index_offset + direction * list_to_search.index(element)
    except ValueError:
        return not_found
