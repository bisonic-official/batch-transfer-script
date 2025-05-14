"""Main script to run the batch transfer."""

from src.parser import build_parser
from src.config import load_config
from src.holders import parse_holders
from src.holders import save_transactions
from src.contract import batch_transfer


def main(config_path):
    """Main function."""

    # Load config file
    config = load_config(config_path)

    # Parse holders
    holders_file = config["event"]["holders"]
    addresses, amounts = parse_holders(holders=holders_file, from_file=True)

    # Transfer to holders
    block_size = int(config["event"]["block_size"])
    txn_receipts = batch_transfer(config, addresses, amounts, block_size)
    print(f"[INFO] Number of transactions performed: {len(txn_receipts)}")

    # Save transactions in file
    save_transactions(config, txn_receipts)


if __name__ == "__main__":
    # Parse arguments
    parser = build_parser()
    args = parser.parse_args()

    # Run main
    main(args.config)
