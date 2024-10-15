# -*- coding: utf-8 -*-
"""
@File        : log.py
@Author      : JunL
@Time        : 2024/3/14 14:44
@Description :
"""
import datetime
from pathlib import Path

from loguru import logger

today = datetime.datetime.today()
formatted_date = today.strftime("%Y-%m-%d")
parent_path = Path(__file__).parent.parent


def add_logger(name="monitor"):
    logger.add(parent_path / f"logs/{name}/{formatted_date}.log", retention="30 days",
               filter=lambda record: record["extra"]["name"] == name)
    name_logger = logger.bind(name=name)
    return name_logger


monitor_logger = add_logger("monitor")
