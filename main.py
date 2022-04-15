from nextcord.ext import commands
from sqlalchemy.exc import ResourceClosedError

from sqlalchemy import text
from alchemy import Session, engine

from os import getenv

bot = commands.Bot(command_prefix='!')

local_session = Session(bind=engine)


@bot.command(name='ping')
async def ping_pong(ctx: commands.Context):
	await ctx.reply('pong! (with nextcord)')


@bot.command(name='raw')
async def execute_raw(ctx: commands.Context, *args: str):
	sql_statement = ''
	for arg in args:
		sql_statement += f' {arg}'
	sql_statement = sql_statement[1:]  # Remove starting whitespace.

	results = local_session.execute(text(sql_statement))

	try:
		# This is important because if results are requested from say, an INSERT statement, an error gets thrown out.
		await ctx.reply(f'SQL QUERY: `{sql_statement}`\nRESULTS: {results.fetchone()}')
	except ResourceClosedError:
		await ctx.reply(f'SQL QUERY: `{sql_statement}`')
	local_session.commit()


@bot.event
async def on_ready():
	print(f'{bot.user.name} is running.')

bot.run(getenv('DISCORD_TOKEN'))
