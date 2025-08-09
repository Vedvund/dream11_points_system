from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field, func, Relationship


class TournamentStatus(str, Enum):
    UPCOMING = "upcoming"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Tournament(SQLModel, table=True):
    __tablename__ = 'tournaments'

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    num_matches: int
    table_head_color: str
    table_index_color: str
    entry_amount: int
    status: TournamentStatus
    created_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()})

    matches: list["Match"] = Relationship(back_populates="tournament")
    prize_money: list["TournamentPrizeMoney"] = Relationship(back_populates="tournament")
    player_tournaments: list["PlayerTournament"] = Relationship(back_populates="tournament")


class Player(SQLModel, table=True):
    __tablename__ = 'players'

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    dream11_name: str
    telegram_id: str
    whatsapp_number: str
    created_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()})

    player_tournaments: list["PlayerTournament"] = Relationship(back_populates="player")
    match_points: list["PlayerMatchPoints"] = Relationship(back_populates="player")


class TournamentPrizeMoney(SQLModel, table=True):
    __tablename__ = 'tournament_prize_money'

    id: Optional[int] = Field(default=None, primary_key=True)
    tournament_id: int = Field(foreign_key="tournaments.id")
    position: int
    amount: int
    created_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()})

    tournament: Tournament = Relationship(back_populates="prize_money")


class Match(SQLModel, table=True):
    __tablename__ = 'matches'

    id: Optional[int] = Field(default=None, primary_key=True)
    tournament_id: int = Field(foreign_key="tournaments.id")
    name: str
    is_abandon: bool = False
    created_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()})

    tournament: Tournament = Relationship(back_populates="matches")
    player_points: list["PlayerMatchPoints"] = Relationship(back_populates="match")


class PlayerTournament(SQLModel, table=True):
    __tablename__ = 'player_tournaments'

    id: Optional[int] = Field(default=None, primary_key=True)
    player_id: int = Field(foreign_key="players.id")
    tournament_id: int = Field(foreign_key="tournaments.id")
    created_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()})

    player: Player = Relationship(back_populates="player_tournaments")
    tournament: Tournament = Relationship(back_populates="player_tournaments")


class PlayerMatchPoints(SQLModel, table=True):
    __tablename__ = 'player_match_points'

    id: Optional[int] = Field(default=None, primary_key=True)
    player_id: int = Field(foreign_key="players.id")
    match_id: int = Field(foreign_key="matches.id")
    points: float
    created_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()})

    player: Player = Relationship(back_populates="match_points")
    match: Match = Relationship(back_populates="player_points")
