import globals

@globals.client.event
async def on_ready():
    globals.client.load_extension('bot.commands')
    print(f'ready as {globals.client.user}')

