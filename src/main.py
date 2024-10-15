from web3 import Web3

from src.log import monitor_logger
from src.monitor import Monitor


async def get_block_height(contract_task_id):
    contract_queryset = await ContractConfig.filter(id=contract_task_id).first()
    if not contract_queryset:
        raise
    scanned_block = contract_queryset.scanned_block

    w3 = Web3(Web3.HTTPProvider(contract_queryset.rpc_url))
    block_number = w3.eth.get_block_number()
    monitor_logger.info(f"block_number: {block_number}")

    to_block = min(scanned_block + contract_queryset.step, block_number)
    monitor_logger.info(f"from_block: {scanned_block}; to_block: {to_block}")
    return scanned_block, to_block, \
           (contract_queryset.rpc_url, contract_queryset.contract_address,
            contract_queryset.contract_event_name, contract_queryset.contract_abi_path)


async def run(contract_task_id):
    # block height
    from_block, to_block, \
        (rpc_url, contract_address, contract_event_name, contract_abi_path) = await get_block_height(contract_task_id)

    if from_block > to_block:
        monitor_logger.info(f"continue")

    # get entries
    obj = Monitor(
        from_block=from_block,
        to_block=to_block,
        rpc_url=rpc_url,
        contract_address=contract_address,
        contract_event=contract_event_name,
        contract_abi_path=contract_abi_path,
    )
    entries = obj.get_entries()
