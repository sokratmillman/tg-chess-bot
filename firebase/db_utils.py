def generate_new_history(current_history, res, partner_id="AI"):
    splitted_history = current_history.split(', ')
    new_history_list = [f"{res} {partner_id}"]

    if len(splitted_history) >=5:
        new_history_list += splitted_history[:-1]
    else:
        new_history_list += splitted_history

    new_history = ', '.join(new_history_list)

    return new_history
