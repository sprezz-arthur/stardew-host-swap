import re


TRANSFERRABLE_MAILS = [
    "<string>ccDoorUnlock</string>",
    "<string>ccPantry</string>",
    "<string>ccCraftsRoom</string>",
    "<string>ccFishTank</string>",
    "<string>ccBoilerRoom</string>",
    "<string>ccBulletin</string>",
    "<string>ccVault</string>",
    "<string>jojaPantry</string>",
    "<string>jojaCraftsRoom</string>",
    "<string>jojaFishTank</string>",
    "<string>jojaBoilerRoom</string>",
    "<string>jojaVault</string>",
    "<string>JojaMember</string>",
    "<string>spring_2_1</string>",  # Willy's shop unlock
]

TRANSFERRABLE_EVENTS = [
    "<int>65</int>",  # Bats or mushrooms
    "<int>1590166</int>",  # Marnie gives you a cat
    "<int>897405</int>",  # Marnie gives you a dog
    "<int>611439</int>",  # Community center unlocked
    "<int>191393</int>",  # Community center final cutscene
    "<int>502261</int>",  # Joja final cutscene
]


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


def get_all_events(input_string: str) -> list[str]:
    pattern = r"<eventsSeen>(.*?)<\/eventsSeen>"
    match = re.search(pattern, input_string)
    if match:
        mails_str = match.group(1)
        pattern = r"<int>(.*?)<\/int>"
        matches = re.findall(pattern, mails_str)
        return [f"<int>{match}</int>" for match in matches]
    else:
        return None


def add_mails(
    giver_data: str,
    taker_data: str,
) -> str:
    giver_mails = get_all_mails(giver_data)
    taker_mails = get_all_mails(taker_data)
    old_mails_data: str = "<mailReceived>" + "".join(taker_mails) + "</mailReceived>"
    for mail in giver_mails:
        if mail not in taker_mails and mail in TRANSFERRABLE_MAILS:
            taker_mails += [mail]
    new_mails_data: str = "<mailReceived>" + "".join(taker_mails) + "</mailReceived>"
    taker_data = taker_data.replace(old_mails_data, new_mails_data)
    return taker_data


def add_events(
    giver_data: str,
    taker_data: str,
) -> str:
    giver_events = get_all_events(giver_data)
    taker_events = get_all_events(taker_data)
    old_mails_data: str = "<eventsSeen>" + "".join(taker_events) + "</eventsSeen>"
    for event in giver_events:
        if event not in taker_events and event in TRANSFERRABLE_EVENTS:
            taker_events += [event]
    new_mails_data: str = "<eventsSeen>" + "".join(taker_events) + "</eventsSeen>"
    taker_data = taker_data.replace(old_mails_data, new_mails_data)
    return taker_data


def get_home_data(player_data: str) -> str:
    home = player_data.split("<homeLocation>")[1].split("</homeLocation>")[0]
    return f"<homeLocation>{home}</homeLocation>"
