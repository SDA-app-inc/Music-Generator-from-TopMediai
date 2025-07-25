"""Initial migration

Revision ID: 37e085568a88
Revises: 
Create Date: 2025-06-24 21:04:40.162602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37e085568a88'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('applications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bundle_id', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('bundle_id')
    )
    op.create_index(op.f('ix_applications_id'), 'applications', ['id'], unique=False)
    op.create_table('request_stats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('app_id', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_request_stats_id'), 'request_stats', ['id'], unique=False)
    op.create_table('templates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('prompt', sa.Text(), nullable=True),
    sa.Column('status', sa.Enum('ACTIVE', 'INACTIVE', name='templatestatus'), nullable=True),
    sa.Column('category', sa.Enum('TRENDING', 'GENERAL', 'CLASSIC', name='templatecategory'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_templates_id'), 'templates', ['id'], unique=False)
    op.create_table('application_templates',
    sa.Column('application_id', sa.Integer(), nullable=False),
    sa.Column('template_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['application_id'], ['applications.id'], ),
    sa.ForeignKeyConstraint(['template_id'], ['templates.id'], ),
    sa.PrimaryKeyConstraint('application_id', 'template_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('application_templates')
    op.drop_index(op.f('ix_templates_id'), table_name='templates')
    op.drop_table('templates')
    op.drop_index(op.f('ix_request_stats_id'), table_name='request_stats')
    op.drop_table('request_stats')
    op.drop_index(op.f('ix_applications_id'), table_name='applications')
    op.drop_table('applications')
    # ### end Alembic commands ###
