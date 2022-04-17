from nextcord.ext import commands
import nextcord

from sqlalchemy import text
from sqlalchemy.exc import ResourceClosedError
from cogs.alchemy import Session, engine

from os import getenv, listdir

bot = commands.Bot(command_prefix='!')

local_session = Session(bind=engine)

intents = nextcord.Intents.default()
intents.members = True


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
		await ctx.reply(f'SQL QUERY: `{sql_statement}`\nRESULTS: {results.fetchall()}')
	except ResourceClosedError:
		await ctx.reply(f'SQL QUERY: `{sql_statement}`')
	local_session.commit()


@bot.event
async def on_ready():
	print(f'{bot.user.name} is running.')

# Dynamically load cogs.
for file in listdir('./cogs/'):
	# Files which should NOT be loaded as cogs.
	WHITELISTED_FILES = ['__init__.py', 'alchemy.py']

	if file not in WHITELISTED_FILES:
		if file.endswith('.py'):
			bot.load_extension(f"cogs.{file[:-3]}")
			print(f"{file} loaded.")

bot.run(getenv('DISCORD_TOKEN'))
