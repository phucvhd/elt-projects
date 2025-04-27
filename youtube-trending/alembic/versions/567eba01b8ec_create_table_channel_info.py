"""create table channel info

Revision ID: 567eba01b8ec
Revises: 7da407a0873f
Create Date: 2025-04-27 16:05:14.343247

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '567eba01b8ec'
down_revision: Union[str, None] = '7da407a0873f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("channel_info",
                    sa.Column('channel_id', sa.Text, primary_key=True),
                    sa.Column('channel_title', sa.Text, nullable=False),
                    sa.Column('country', sa.Text, nullable=False),
                    sa.Column('published_at', sa.TIMESTAMP, nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("channel_info")
    pass
