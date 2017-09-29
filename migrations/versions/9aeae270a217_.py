"""empty message

Revision ID: 9aeae270a217
Revises: 
Create Date: 2017-09-28 23:58:51.923678

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9aeae270a217'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'property',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('address', sa.String(length=255), nullable=True),
        sa.Column('suburb_name', sa.String(length=255), nullable=True),
        sa.Column('property_type', sa.String(length=100), nullable=True),
        sa.Column('bedrooms', sa.Integer(), nullable=True),
        sa.Column('bathrooms', sa.Integer(), nullable=True),
        sa.Column('carparks', sa.Integer(), nullable=True),
        sa.Column('land_size', sa.Integer(), nullable=True),
        sa.Column('price', sa.Float(), nullable=True),
        sa.Column('sold_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('link', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('property')
    # ### end Alembic commands ###
