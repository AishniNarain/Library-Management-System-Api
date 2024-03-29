"""empty message

Revision ID: 88b9ae1c5083
Revises: b2fb747d435b
Create Date: 2024-03-22 15:39:51.337191

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '88b9ae1c5083'
down_revision = 'b2fb747d435b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('borrow_books')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('borrow_books',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('issue_date', sa.DATE(), nullable=True),
    sa.Column('due_date', sa.DATE(), nullable=True),
    sa.Column('issued_by', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('fine', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('fine_days', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('status', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('return_date', sa.DATE(), nullable=True),
    sa.Column('student_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('books_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('expected_return_date', sa.DATE(), nullable=True),
    sa.ForeignKeyConstraint(['books_id'], ['books.id'], name='borrow_books_ibfk_1'),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], name='borrow_books_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
