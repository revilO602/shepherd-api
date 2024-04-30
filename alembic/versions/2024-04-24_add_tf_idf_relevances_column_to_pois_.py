"""add tf_idf_relevances column to pois table

Revision ID: bc344545df18
Revises: 2baf1f97892e
Create Date: 2024-04-24 20:33:12.919118

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'bc344545df18'
down_revision: Union[str, None] = '2baf1f97892e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pois', sa.Column('tf_idf_relevances', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pois', 'tf_idf_relevances')
    # ### end Alembic commands ###