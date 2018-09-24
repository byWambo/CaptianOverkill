import discord
from discord.ext import commands
import humanify


class Post:
    def __init__(self, msg: discord.Message, bot: discord.ext.commands.Bot):
        self.msg = msg
        self.bot = bot
        self.likes = 0

    def add_like(self):
        self.likes += 1


class Instacord:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def post(self, ctx: discord.ext.commands.Context, *, post: str):

        likes = 0
        await ctx.message.add_reaction('❤')

    @commands.command()
    async def posts(self, ctx: discord.ext.commands.Context):
        output = ''
        for i in self.bot.posts:
            output += 'Post von ' + i.msg.author.name + ' um ' + humanify.datetime(i.msg.created_at) + ' : ' + \
                      i.msg.content + ' | ' + str(i.likes) + ' Likes\n'
        if output != '':
            await ctx.send(output)
        else:
            await ctx.send('Keine Posts da!')

    async def on_reaction_add(self, reaction, user):
        found = False
        if reaction.emoji == '❤':
            for i in self.bot.posts:
                if i.msg == reaction.message:
                    i.add_like()
                    found = True
            if found is False:
                tempmsg = reaction.message
                tempmsg.content = tempmsg.content.replace('>post ', '')
                thread = Post(msg=reaction.message, bot=self.bot)
                self.bot.posts.insert(0, thread)
                if len(self.bot.posts) >= 11:
                    self.bot.posts.pop(10)

    @commands.command()
    async def clear_posts(self, ctx):
        if ctx.author.id == self.bot.G3eID:
            self.bot.posts = []
            await ctx.send('Cleared')

    @post.error
    async def post_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Benutzung: >post <Inhalt> - Beispiel >gif I'm completely overkill")


def setup(bot: commands.bot):
    bot.add_cog(Instacord(bot=bot))
