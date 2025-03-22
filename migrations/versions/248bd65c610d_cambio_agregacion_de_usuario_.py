"""Cambio agregacion de usuario, organigrama y nodos

Revision ID: 248bd65c610d
Revises: 
Create Date: 2025-03-21 14:46:56.579574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '248bd65c610d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('nodos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('organigrama_id', sa.Integer(), nullable=False))
        batch_op.alter_column('tipo_cargo',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.create_foreign_key(None, 'organigramas', ['organigrama_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('nodos', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('tipo_cargo',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)
        batch_op.drop_column('organigrama_id')

    # ### end Alembic commands ###
