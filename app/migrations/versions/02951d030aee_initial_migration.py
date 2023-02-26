"""Initial migration.

Revision ID: 02951d030aee
Revises:
Create Date: 2023-02-27 00:08:26.971082

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "02951d030aee"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=50), nullable=False),
        sa.Column("phone", sa.String(length=50), nullable=False),
        sa.Column("first_name", sa.String(length=50), nullable=False),
        sa.Column("last_name", sa.String(length=50), nullable=False),
        sa.Column("birth_date", sa.Date(), nullable=False),
        sa.Column("date_created", sa.DateTime(), nullable=False),
        sa.Column("date_modified", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("phone"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "purses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "currency",
            sa.Enum("USD", "EUR", "GBP", "UAH", name="currency"),
            nullable=False,
        ),
        sa.Column("balance", sa.Float(), nullable=False),
        sa.Column("date_created", sa.DateTime(), nullable=False),
        sa.Column("date_modified", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("purse_from_id", sa.Integer(), nullable=False),
        sa.Column("purse_to_id", sa.Integer(), nullable=False),
        sa.Column(
            "purse_from_currency",
            sa.Enum("USD", "EUR", "GBP", "UAH", name="currency"),
            nullable=False,
        ),
        sa.Column(
            "purse_to_currency",
            sa.Enum("USD", "EUR", "GBP", "UAH", name="currency"),
            nullable=False,
        ),
        sa.Column("purse_from_amount", sa.Float(), nullable=False),
        sa.Column("purse_to_amount", sa.Float(), nullable=False),
        sa.Column("date_created", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["purse_from_id"],
            ["purses.id"],
        ),
        sa.ForeignKeyConstraint(
            ["purse_to_id"],
            ["purses.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("transactions")
    op.drop_table("purses")
    op.drop_table("users")
    # ### end Alembic commands ###