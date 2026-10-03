"""add embeddings to code chunks"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


revision: str = "215f76e44288"
down_revision: Union[str, None] = "cb0b0d0a0d99"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.add_column(
        "code_chunks",
        sa.Column(
            "embedding",
            Vector(dim=1536),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("code_chunks", "embedding")