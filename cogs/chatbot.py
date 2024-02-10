import re
import discord
import g4f
from discord import app_commands
from discord.ext import commands
from loguru import logger
from lib.prompts import gpt_prompts
from typing import Literal

import config
from utils.connection import Connection as Conn


class ChatbotCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prompt = gpt_prompts["waffle"]

    @app_commands.command(name="chatbot_status", description="get engine and")
    async def chatbot_status(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f">>> **Engine**: {self.engine}\n**Prompt**: {self.prompt}"
        )

    # @app_commands.command(
    #     name="gpt",
    #     description="Send a raw prompt to GPT.",
    # )
    # async def gpt(self, interaction: discord.Interaction, prompt: str):
    #     await interaction.response.defer(thinking=True)
    #     response = await openai.ChatCompletion.acreate(
    #         temperature=0.7, max_tokens=2048, engine=self.engine, prompt=prompt
    #     )
    #     logger.info(f"GPT recvd: {response}")
    #     await interaction.followup.send(
    #         f">>> {prompt}\n```\n{response.choices[0].text[-4500:]}\n```"
    #     )

    # @app_commands.command(name="bj", description="im cheating at blackjack")
    # async def bj(
    #     self, interaction: discord.Interaction, dealer: str, up1: str, up2: str
    # ):
    #     await interaction.response.defer(thinking=True)
    #     messages = [
    #         {
    #             "role": "system",
    #             "content": "You will act as an expert of blackjack. I will tell you the upcards, and you will advise me on my best course of action with some blackjack slang. Don't explain rules. Just math and what to do based on what a blackjack expert would do. Please repeat the cards in play with your response.",
    #         },
    #         {
    #             "role": "user",
    #             "content": f"blackjack: dealer has {dealer}. I have {up1}, {up2}.",
    #         },
    #     ]
    #     response = await openai.ChatCompletion.acreate(
    #         temperature=0.7,
    #         max_tokens=1024,
    #         model=self.engine,
    #         messages=messages,
    #     )
    #     logger.info(f"Response recvd. Tokens used: {response['usage']['total_tokens']}")
    #     await interaction.followup.send(response.choices[0].message.content)

    # @app_commands.command(name="setengine")
    # async def setengine(
    #     self,
    #     interaction: discord.Interaction,
    #     engines: Literal["gpt-4", "gpt-3.5-turbo"],
    # ):
    #     self.engine = engines
    #     await interaction.response.send_message(f"Engine set to {engines}")

    # @app_commands.command(name="setprompt")
    # async def setprompt(
    #     self,
    #     interaction: discord.Interaction,
    #     prompts: Literal["waffle", "jailbreak", "qb"],
    # ):
    #     if prompts == "waffle":
    #         self.prompt = gpt_prompts["waffle"]
    #         await interaction.response.send_message("Prompt set to WAFFLE.")
    #     elif prompts == "jailbreak":
    #         self.prompt = gpt_prompts["jailbreak"]
    #         await interaction.response.send_message("Prompt set to Jailbreak.")
    #     elif prompts in gpt_prompts:
    #         self.prompt = gpt_prompts[prompts]
    #         await interaction.response.send_message(f"Prompt set to {prompts}")

    @app_commands.command(name="character_prompt")
    async def character_prompt(
        self, interaction: discord.Interaction, character: str, series: str
    ):
        prompt = (
            f"The following is a conversation between {character} from {series} and a friend. Respond and answer "
            f"like {character} using the tone, manner and vocabulary {character} would use. Do not write any "
            f"explanations. Only answer like {character}. You must know all of the knowledge of {character}."
        )
        self.prompt = prompt
        await interaction.response.send_message(
            f"Prompt set to {character} from {series}."
        )

    # @app_commands.command(
    #     name="dream",
    #     description="Generate an image based on a prompt.",
    # )
    # async def dream(self, interaction: discord.Interaction, prompt: str):
    #     try:
    #         await interaction.response.defer(thinking=True)
    #         response = await openai.Image.acreate(prompt=prompt, n=1, size="512x512")
    #         image_url = response["data"][0]["url"]
    #         filename = prompt
    #         if len(filename) > 100:
    #             filename = filename[:100]
    #         filename = re.sub(r"[^\w\s]", "", filename.lower())
    #         filename = re.sub(r"\s+", "-", filename)
    #         async with Conn() as resp:
    #             logger.info(f"Image recvd: {image_url}")
    #             image = await resp.read(image_url)
    #             # add if file exists check
    #             with open(f"dreams/{filename}.png", "wb") as f:
    #                 f.write(image)
    #         await interaction.followup.send(
    #             f"`{prompt}`", file=discord.File(f"dreams/{filename}.png")
    #         )
    #     except openai.InvalidRequestError:
    #         await interaction.followup.send("Too offensive. :(")
    #     except Exception as e:
    #         logger.exception(e)
    #         await interaction.followup.send("Something went wrong. :(")

    @commands.Cog.listener()
    async def on_message(self, message):
        # logger.info(f"Message sent: {message.content}")
        messages = [
            {"role": "system", "content": self.prompt},
            # {"role": "user", "content": i},
        ]
        send = 0
        if message.channel.id not in config.IGNORE_CHANNELS:
            if message.reference:
                replied_message = await message.channel.fetch_message(
                    message.reference.message_id
                )
                if replied_message.author.id == 968919979577704529:
                    m = [
                        {"role": "assistant", "content": replied_message.content},
                        {"role": "user", "content": message.content},
                    ]
                    if replied_message.reference:
                        second_reply = await message.channel.fetch_message(
                            replied_message.reference.message_id
                        )
                        m = [{"role": "user", "content": second_reply.content}] + m
                        if second_reply.reference:
                            third_reply = await message.channel.fetch_message(
                                second_reply.reference.message_id
                            )
                            m = [
                                {"role": "assistant", "content": third_reply.content}
                            ] + m

                    messages = messages + m
                    logger.info(f"Input sent: {m}")
                    send = 1
            elif "<@968919979577704529>" in message.content or (
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
                    model=g4f.models.gpt_4,
                    messages=messages,
                    provider=g4f.Provider.Bing,
                )
                r = response
                # self.previous_messages.append("Waffle: " + response + " ")
                # print(f"previous_messages: {''.join(self.previous_messages)}")
                # chat limit is 2000 chars
                if len(r) > 2000:
                    r = r[:2000]
                await message.reply(r, mention_author=False)
            except Exception as e:
                logger.exception(e)
                await message.channel.send(e.__class__.__name__)


async def setup(bot):
    await bot.add_cog(ChatbotCog(bot))
