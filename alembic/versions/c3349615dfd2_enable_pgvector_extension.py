"""Enable pgvector extension

Revision ID: c3349615dfd2
Revises:
Create Date: 2025-02-24 04:40:36.845307

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "c3349615dfd2"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    """Enable the pgvector extension in PostgreSQL."""
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")


def downgrade():
    """Optionally disable the pgvector extension on downgrade."""
    op.execute("DROP EXTENSION IF EXISTS vector;")
