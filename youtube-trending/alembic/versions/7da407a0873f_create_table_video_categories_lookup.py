"""create table video_categories_lookup

Revision ID: 7da407a0873f
Revises: 99431fb8a00c
Create Date: 2025-04-25 16:47:06.022321

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7da407a0873f'
down_revision: Union[str, None] = '99431fb8a00c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("video_categories_lookup",
                    sa.Column('category_id', sa.Integer, primary_key=True),
                    sa.Column('category_name', sa.Text, nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('video_categories_lookup')
    pass
