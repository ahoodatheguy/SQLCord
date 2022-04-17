from nextcord.ext import commands
from .alchemy import Session, engine, Base
from prettytable import PrettyTable
from sqlalchemy.inspection import inspect


class ReadCommands(commands.Cog):
	def __init__(self, bot) -> None:
		self.bot = bot
		self.session = Session(bind=engine)

	@commands.command(name="table", description="Get an overview of a tables data.")
	async def view_table(self, ctx: commands.Context, table: str):
		table_obj = getattr(Base.classes, table)
		column_names = [column.name for column in inspect(table_obj).c]  # Get list of column names.
		query = self.session.query(table_obj).all()[:3]  # Show a max of 3 rows.

		# Create ASCII table
		ascii_table = PrettyTable()
		ascii_table.field_names = column_names

		# Dynamically create ASCII table columns and rows.
		for i in query:
			row_list = []
			for column in column_names:
				row_list.append(getattr(i, column))
			ascii_table.add_row(row_list)

		await ctx.reply(f'```{ascii_table}```')


def setup(bot: commands.Bot):
	bot.add_cog(ReadCommands(bot))
