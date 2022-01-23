import discord
from discord.ext import commands
from discord_slash.utils.manage_components import (
    create_select,
    create_select_option,
    create_actionrow,
    wait_for_component,
    ComponentContext
)
import time


class ExampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        select = create_select(
            options=[  # the options in your dropdown
                create_select_option("Music commands", value="music"),
                create_select_option("Moderation commands", value="mod"),
                create_select_option("Mini-games commands", value="games"),
            ],
            placeholder="Choose your option",  # the placeholder text to show when no options have been chosen
            min_values=1,  # the minimum number of options a user must select
            max_values=1,  # the maximum number of options a user can select
        )
        await ctx.send("test", components=[create_actionrow(select)])

        t_end = time.time() + 60
        while time.time() < t_end:
            button_ctx: ComponentContext = await wait_for_component(self.bot, components=select, timeout=60)
            # TODO: edit this part with real commands
            if button_ctx.selected_options[0] == "music":
                await button_ctx.edit_origin(content="You pressed a to music!")
            if button_ctx.selected_options[0] == "mod":
                await button_ctx.edit_origin(content="You pressed a to mod!")
            if button_ctx.selected_options[0] == "games":
                await button_ctx.edit_origin(content="You pressed a to games!")


def setup(bot):
    bot.add_cog(ExampleCog(bot))
