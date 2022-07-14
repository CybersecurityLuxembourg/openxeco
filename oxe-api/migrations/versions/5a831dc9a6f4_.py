"""empty message

Revision ID: 5a831dc9a6f4
Revises: a6f02c599c2f
Create Date: 2022-07-14 12:09:14.511955

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision = '5a831dc9a6f4'
down_revision = 'a6f02c599c2f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('CompanyRelationshipType',
    sa.Column('name', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=100), nullable=False),
    sa.PrimaryKeyConstraint('name'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )

    op.create_table('CompanyRelationship',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('company_1', mysql.INTEGER(), nullable=False),
    sa.Column('type', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=100), nullable=False),
    sa.Column('company_2', mysql.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['company_1'], ['Company.id'], name='companyrelationship_ibfk_1', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['type'], ['CompanyRelationshipType.name'], name='companyrelationship_ibfk_2', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['company_2'], ['Company.id'], name='companyrelationship_ibfk_3', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )

    op.rename_table('Company_Address', 'CompanyAddress')


def downgrade():
    op.drop_table('CompanyRelationship')
    op.drop_table('CompanyRelationshipType')

    op.rename_table('CompanyAddress', 'Company_Address')
