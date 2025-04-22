"""create raw_youtube_trending table

Revision ID: 99431fb8a00c
Revises: 
Create Date: 2025-04-22 17:04:16.495172

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import func

# revision identifiers, used by Alembic.
revision: str = '99431fb8a00c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("raw_youtube_trending",
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('raw_json', sa.JSON, nullable=False),
                    sa.Column('fetch_timestamp', sa.TIMESTAMP, server_default=func.now()))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('raw_youtube_trending')
    pass
