from discord.utils import find
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context
from discord.ext.commands import CommandNotFound, BadArgument
from discord.ext.commands import MissingRequiredArgument, MissingRole, MissingPermissions
from discord.errors import Forbidden
from discord import Embed, File
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
from glob import glob
from datetime import datetime 
from asyncio import sleep

PREFIX = "&"
OWNER_IDS = [572353145963806721,524309352698609684]
COMMANDS = [path.split("\\")[-1][:-3] for path in glob("./lib/commands/*.py")]
IGNORE_EXCEPTIONS = [CommandNotFound, BadArgument]
class Ready(object):
    def __init__(self):
        for command in COMMANDS:
            setattr(self, command, False)
    def ready_up(self, command):
        setattr(self, command, True)
        print(f"{command} command is ready")

    def all_ready(self):
        return all([getattr(self, command) for command in COMMANDS])

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.command_ready = Ready()
        self.guild = None
        # self.scheduler = AsyncIOScheduler()

        super().__init__(command_prefix=PREFIX, OWNER_ID=OWNER_IDS)

    def setup(self):
        print("setup Run")
        for command in COMMANDS:
            self.load_extension(f"lib.commands.{command}") ## Checkn and Debug
            print(f"{command} cog Loaded")

    def run(self, version):
        self.VERSION = version
        print("running setup")
        self.setup()

        with open("./lib/bot/token", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("Running Gift Bot...")
        super().run(self.TOKEN, reconnect=True)

    async def process_commands(self,message):
        ctx = await self.get_context(message, cls=Context)
        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                await self.invoke(ctx)
            else:
                await self.send("Wait for OtakuStan Bot to be ready!! ")
    
    async def on_connect(self):
        print("Ara Ara!")

    async def on_disconnect(self):
        print("Ara Ara Sionara!")

    async def on_error(self, err, ctx, *args, **kwargs):
        if err == 'on_command_error':
            await ctx.send("An error Occurrred")
        raise 

    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, err) for err in IGNORE_EXCEPTIONS]):
            pass

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("One or More argument required by OtakuStan Bot!!")

        elif isinstance(exc, MissingPermissions):
            await ctx.send("You are not allowed to use the Commands")

        elif isinstance(exc, MissingRole):
            await ctx.send("You do not have the necessary role to use OtakuStan Bot")
        
        elif hasattr(exc, "original"):
            if isinstance(exc.original, Forbidden):
                await ctx.send("OtakuStan Bot doesn't have permission to do that!!")
            else:
                raise exc.original
        else:
            raise exc


    async def on_ready(self):
        if not self.ready:
            while not self.command_ready.all_ready():
                print("waiting......")
                await sleep(0.5)
            self.ready = True
            print("OtakuStan Bot ready")
            # embed = Embed(title="OtakuStan Bot is Now Online", description="You have Otakustan bot into your server to help with your Giveaways", colour=0x00FFFF, timestamp=datetime.utcnow())
            # embed.set_author(name="LoLi Lover")
            # await self.stdout.send(embed=embed)
        else:
            print("OtakuStan Bot reconnected")

    async def on_guild_join(self, guild):
        general = find(lambda x: x.name == 'general', guild.text_channels)
        if general and general.permissions_for(guild.me).send_messages:
            embed = Embed(title="OtakuStan Bot is Now on your server", description="Oniichan/Oneechan!! You have invited OtakuStan bot into your server to help you with your Giveaways", colour=0x00FFFF, timestamp=datetime.utcnow())
            embed.set_author(name=guild.name)
            embed.set_thumbnail(url="https://firebasestorage.googleapis.com/v0/b/sociality-a732c.appspot.com/o/OS%20new%20logo.jpg?alt=media&token=99f4399f-57ae-469a-9ba8-78972bead82a")
            # embed.set_image(url="https://firebasestorage.googleapis.com/v0/b/sociality-a732c.appspot.com/o/Loli.png?alt=media&token=ab5c8924-9a14-40a9-97b8-dba68b69195d")
            await general.send(embed=embed)

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)

bot = Bot()