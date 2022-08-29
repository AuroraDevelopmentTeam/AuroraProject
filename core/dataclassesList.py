from dataclasses import dataclass


@dataclass
class CustomRole:
    guild_id: int
    role_id: int
    cost: int
    owner_id: int
    created: int
    expiration_date: int
    bought: int
