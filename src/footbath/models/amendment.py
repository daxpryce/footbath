from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar

from .zeep_ops import ZeepOps

__all__ = ["Amendment"]


@dataclass
class Amendment(ZeepOps):
    zeep_aliases: ClassVar[Mapping[str, str]] = {
        "type": "amendment_type",
    }

    bill_number: int
    name: str
    bill_id: str
    legislative_session: str
    amendment_type: str
    floor_number: int
    sponsor_name: str
    description: str
    drafter: str
    floor_action: str
    floor_action_date: datetime
    document_exists: bool
    htm_url: str
    pdf_url: str
    agency: str
