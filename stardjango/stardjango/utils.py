import re


# TODO: figure out why this does not work when input_string is too large
def _get_host_data(input_string: str) -> str:
    pattern = r"<player>(.*?)<\/player>"
    match = re.search(pattern, input_string)

    if match:
        return match.group(1)
    else:
        return None


def get_host_data(input_string: str) -> str:
    return input_string.split("<player>")[1].split("</player>")[0]


def get_players_data(input_string: str) -> list[str]:
    pattern = r"<farmhand>(.*?)<\/farmhand>"
    matches = re.findall(pattern, input_string)
    return matches


def get_name(input_string: str) -> str:
    pattern = r"<name>(.*?)<\/name>"
    match = re.search(pattern, input_string)

    if match:
        return match.group(1)
    else:
        return None


def get_all_mails(input_string: str) -> list[str]:
    pattern = r"<mailReceived>(.*?)<\/mailReceived>"
    match = re.search(pattern, input_string)
    if match:
        mails_str = match.group(1)
        pattern = r"<string>(.*?)<\/string>"
        matches = re.findall(pattern, mails_str)
        return [f"<string>{match}</string>" for match in matches]
    else:
        return None


def get_community_center_mails(input_string: str) -> list[str]:
    pattern = r"<string>(cc.*?)<\/string>"
    matches = re.findall(pattern, input_string)
    return [f"<string>{match}</string>" for match in matches]


def add_mails(
    giver_data: str,
    taker_data: str,
) -> str:
    giver_mails = get_all_mails(giver_data)
    taker_mails = get_all_mails(taker_data)
    old_mails_data: str = "<mailReceived>" + "".join(taker_mails) + "</mailReceived>"
    for mail in giver_mails:
        if mail not in taker_mails:
            print(f"Adding mail: {mail}")
            taker_mails += [mail]
    new_mails_data: str = "<mailReceived>" + "".join(taker_mails) + "</mailReceived>"
    taker_data = taker_data.replace(old_mails_data, new_mails_data)
    return taker_data


def add_community_center_mails(giver_data: str, taker_data: str) -> str:
    giver_mails = get_community_center_mails(giver_data)
    taker_mails = get_all_mails(taker_data)
    for mail in giver_mails:
        if mail not in taker_mails:
            taker_mails += [mail]
    return "<mailReceived>" + "".join(taker_mails) + "</mailReceived>"


def get_home_data(player_data: str) -> str:
    home = player_data.split("<homeLocation>")[1].split("</homeLocation>")[0]
    return f"<homeLocation>{home}</homeLocation>"
