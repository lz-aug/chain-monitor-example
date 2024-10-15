# -*- coding: utf-8 -*-
"""
@File        : contract_event.py
@Author      : JunL
@Time        : 2024/3/25 11:20
@Description :
"""
from tortoise import fields

from src.models.base import BaseModel


class ContractConfig(BaseModel):
    name = fields.CharField(max_length=255)
    chain = fields.IntField(null=True)
    contract_address = fields.CharField(max_length=255)
    contract_abi_path = fields.CharField(max_length=100)
    contract_event_name = fields.CharField(max_length=100, description="event name")
    rpc_url = fields.CharField(max_length=255)

    start_block = fields.IntField(default=100, null=True, blank=True)
    scanned_block = fields.IntField(default=100, null=True, blank=True)
    step = fields.IntField(default=2000)
    in_schedule = fields.BooleanField(default=True)

    class Meta:
        table = "contract_config"


class EventLog(BaseModel):
    id = fields.IntField(pk=True)
    blockNumber = fields.IntField(null=True)
    chain = fields.IntField(null=True)
    event_name = fields.CharField(max_length=100, description="event name")
    event_address = fields.CharField(max_length=255, null=True, description="event address")

    logIndex = fields.IntField(default=0)
    transactionHash = fields.CharField(max_length=200, description="tx hash")

    from_address = fields.CharField(max_length=255, null=True, description="from user address")
    to = fields.CharField(max_length=255, null=True, description="to address")
    token = fields.CharField(max_length=255, null=True, description="token address")
    amount = fields.CharField(max_length=100, description="token amount")
    targetChainId = fields.IntField(null=True)
    targetToken = fields.CharField(max_length=255, null=True, description="target token address")
    blockHeight = fields.IntField(null=True)

    sourceChainId = fields.IntField(null=True)
    sourceTxHash = fields.CharField(null=True, max_length=200, description="source hash")
    args = fields.JSONField(default=dict)
    nonce = fields.IntField(null=True)

    class Meta:
        table = "event_log"
