"""Holders utilities."""

import json

DECIMAL_CONVERSION = 1_000_000_000_000_000_000


def parse_holders(holders, from_file=False):
    """Parses the holders json objecto from file or form obj directly.

    Parameters
    ----------
    holders : str or list
        A trsing containing the path of the holders file or the
        list with the holders as a JSON object. This is specified in
        the "from_file" flag.
    from_file : bool
        A flag indicating if a path or a JSON object is provided.

    Returns
    -------
    addresses : list
        The list of addresses.
    amounts : list
        The list of amounts per address.
    """

    if from_file:
        with open(holders, "rt", encoding="utf-8") as f:
            holders = json.load(f)

    addresses, amounts = [], []
    for holder in holders:
        addresses.append(holder["wallet"])
        amounts.append(holder["amount"])

    return addresses, amounts


def save_transactions(config, txn_receipts):
    """Saves transactions list in file.

    Parameters
    ----------
    config : dict
        The config dictionary.
    txn_receipts : list
        A list of strings for transactions performed.
    """

    txns_file = config["event"]["transactions"]

    with open(txns_file, "wt", encoding="utf-8") as f:
        for txn in txn_receipts:
            f.write(txn + "\n")
