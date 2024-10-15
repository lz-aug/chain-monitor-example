from web3 import Web3, HTTPProvider


# -*- coding: utf-8 -*-
"""
@File        : entries.py
@Author      : JunL
@Time        : 2024/3/14 14:55
@Description :
"""
import json
from pathlib import Path

from retrying import retry
from web3 import Web3

from src.log import monitor_logger as logger


current_path = Path(__file__).parent.parent.parent


def load_abi(abi_path: str) -> dict:
    """load contract abi

    Args:
        abi_path (str): Contract abi file name

    Returns:
        contract_abi (dict): contract abi
    """
    abi_path = current_path / "abi" / abi_path
    with open(abi_path) as f:
        contract_abi = json.load(f)
    return contract_abi


class Monitor(object):
    """Get the specific contract event entries"""

    def __init__(self,
                 rpc_url,
                 from_block=None,
                 to_block=None,
                 contract_address=None,
                 contract_event=None,
                 contract_event_filter=None,
                 contract_abi_path=None,
                 security_block=64
                 ):
        """
        Args:
            rpc_url (str): Chain rpc url address.
            from_block (int): The start block height.
            to_block (int): The end block height.
            contract_address (str): contract address.
            contract_event (str): contract event.
            contract_event_filter (dict): Filter the event args condition.
            contract_abi_path (str): contract abi.
            security_block (int): Security block
        """
        self.rpc_url = rpc_url
        self.from_block = from_block
        self.to_block = to_block - security_block
        self.contract_address = contract_address
        self.contract_event = contract_event
        self.contract_event_filter = contract_event_filter or {}
        if contract_abi_path:
            self.contract_abi = load_abi(contract_abi_path)

    @retry(stop_max_attempt_number=3)
    def init_web3(self):
        try:
            w3 = Web3(Web3.HTTPProvider(self.rpc_url))
            logger.info(f"------ connected rpc success.")
            return w3
        except Exception as e:
            logger.error(e)
            raise Exception("------ connected web3 rpc error.")

    def init_contract(self):
        w3 = self.init_web3()
        contract_address = w3.to_checksum_address(self.contract_address)
        my_contract = w3.eth.contract(contract_address, abi=self.contract_abi)
        logger.info(f"------ event_names: {[en.event_name for en in my_contract.events]}.")
        logger.info(f"------ event filter: {self.contract_event}.")
        logger.info(f"------ connected contract success.")
        return my_contract

    def get_entries(self):
        """Getting the entries

        Returns:
            LogReceipt (list): entries
        """
        my_contract = self.init_contract()
        event_func = eval(f"my_contract.events.{self.contract_event}.create_filter")
        event_filter = event_func(
            fromBlock=self.from_block,
            toBlock=self.to_block,
            argument_filters=self.contract_event_filter
        )
        all_entries = event_filter.get_all_entries()
        logger.info(f"all_entries_len: {len(all_entries)}")
        return all_entries
