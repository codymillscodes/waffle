import g4f
from discord.ext import commands
from loguru import logger
from strings.gpt_prompts import gpt_prompts

import config


class ChatbotCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prompt = gpt_prompts["waffle"]

    # @app_commands.command(name="character_prompt")
    # async def character_prompt(
    #     self, interaction: discord.Interaction, character: str, series: str
    # ):
    #     prompt = (
    #         f"The following is a conversation between {character} from {series} and a friend. Respond and answer "
    #         f"like {character} using the tone, manner and vocabulary {character} would use. Do not write any "
    #         f"explanations. Only answer like {character}. You must know all of the knowledge of {character}."
    #     )
    #     self.prompt = prompt
    #     await interaction.response.send_message(
    #         f"Prompt set to {character} from {series}."
    #     )

    @commands.Cog.listener()
    async def on_message(self, message):
        # logger.info(f"Message sent: {message.content}")
        messages = [
            {"role": "system", "content": self.prompt},
            # {"role": "user", "content": i},
        ]
        send = 0
        if message.channel.id not in config.IGNORE_CHANNELS:
            # if message.reference:
            #     replied_message = await message.channel.fetch_message(
            #         message.reference.message_id
            #     )
            #     if replied_message.author.id == 968919979577704529:
            #         m = [
            #             {"role": "assistant", "content": replied_message.content},
            #             {"role": "user", "content": message.content},
            #         ]
            #         if replied_message.reference:
            #             second_reply = await message.channel.fetch_message(
            #                 replied_message.reference.message_id
            #             )
            #             m = [{"role": "user", "content": second_reply.content}] + m
            #             if second_reply.reference:
            #                 third_reply = await message.channel.fetch_message(
            #                     second_reply.reference.message_id
            #                 )
            #                 m = [
            #                     {"role": "assistant", "content": third_reply.content}
            #                 ] + m

            #         messages = messages + m
            if "<@968919979577704529>" in message.content or (
                len(message.mentions) > 0 and "waffle" in message.mentions[0].name
            ):
                # logger.info(f"{message.channel.id} | {config.IGNORE_CHANNELS}")
                logger.info(message.type)
                logger.info(message.content)
                ctx = await self.bot.get_context(message)
                i = message.content
                async with ctx.typing():
                    i = i.replace("<@968919979577704529>", "")
                    messages.append({"role": "user", "content": i})
                    logger.info(f"Input sent: {i}")
                    send = 1
        if send == 1:
            try:
                response = await g4f.ChatCompletion.create_async(
                    model="mixtral-8x22b",
                    messages=messages,
                    provider=g4f.Provider.DeepInfra,
                )
                r = response
                if len(r) > 2000:
                    r = r[:2000]
                await message.reply(r, mention_author=False)
            except Exception as e:
                logger.exception(e)
                await message.channel.send(e.__class__.__name__)


async def setup(bot):
    await bot.add_cog(ChatbotCog(bot))
