from discord.ext import commands
import discord
import openai
import re
from loguru import logger
import config
from utils.connection import Connection as Conn

ENGINE = "text-davinci-003"
CHAT_ENGINE = "gpt-3.5-turbo"
openai.api_key = config.OPENAI_KEY


class ChatbotCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.previous_messages = []
        openai.aiosession.set(Conn())

    @commands.command(
        name="gpt",
        description="Send a raw prompt to GPT.",
        brief="Send a raw prompt to GPT.",
    )
    async def gpt(self, ctx, *, input: str):
        response = await openai.Completion.acreate(
            temperature=0.9, max_tokens=512, engine=ENGINE, prompt=input
        )
        logger.info(f"GPT recvd: {response}")
        await ctx.reply(
            f">>> {input}\n```\n{response.choices[0].text[-4500:]}\n```",
            mention_author=False,
        )

    @commands.command(
        name="dream",
        brief="Generate an image based on a prompt.",
        description="Generate an image based on a prompt.",
    )
    async def dream(self, ctx, *, input: str):
        try:
            response = await openai.Image.acreate(prompt=input, n=1, size="512x512")
            image_url = response["data"][0]["url"]
            filename = input
            if len(filename) > 100:
                filename = filename[:100]
            filename = re.sub(r"[^\w\s]", "", filename.lower())
            filename = re.sub(r"\s+", "-", filename)
            async with Conn() as resp:
                logger.info(f"Image recvd: {image_url}")
                image = await resp.read(image_url)
                # add if file exists check
                with open(f"dreams/{filename}.png", "wb") as f:
                    f.write(image)
            await ctx.reply(
                file=discord.File(f"dreams/{filename}.png"), mention_author=False
            )
        except openai.InvalidRequestError:
            await ctx.send("Too offensive. :(")
        except Exception as e:
            logger.exception(e)
            await ctx.send("Something went wrong. :(")

    @commands.Cog.listener()
    async def on_message(self, message):
        # if message.author.id == 295285994607869953:
        #    hl_cmd = self.bot.get_command("hogwarts")
        #    ctx = await self.bot.get_context(message)
        #    await ctx.invoke(hl_cmd)
        if message.reference is None:
            if message.content.startswith("@waffle") or (
                len(message.mentions) > 0 and "waffle" in message.mentions[0].name
            ):
                logger.info(message.type)
                ctx = await self.bot.get_context(message)
                i = message.content
                async with ctx.typing():
                    if message.content.startswith(
                        "<@968919979577704529>"
                    ) or message.content.startswith("@waffle"):
                        logger.info(f"Input sent: {i}")
                        try:
                            prompt = "The following is a conversation with an AI assistant named Waffle. We're trapped in the belly of this horrible machine and the machine is bleeding to death. The assistant is creative, clever, sarcastic and cusses a lot."
                            messages = [{"role": "system", "content": prompt}, {"role": "user", "content": "Hello, who are you?"}, {"role": "assistant", "content" : "I'm Waffle, a fuckin AI created by OpenAI. How the fuck can I help you today?"}, {"role": "user", "content": i}]
                            response = await (
                                openai.ChatCompletion.acreate(
                                    temperature=0.9,
                                    max_tokens=1024,
                                    engine=CHAT_ENGINE,
                                    messages=messages,
                                )
                            )
                            response = response.choices[0].message.content
                            logger.info(f"Response recvd: {response}")
                            # self.previous_messages.append("Waffle: " + response + " ")
                            # print(f"previous_messages: {''.join(self.previous_messages)}")
                            # chat limit is 2000 chars
                            if len(response) > 2000:
                                response = response[:2000]
                            await message.reply(response, mention_author=False)
                        except Exception as e:
                            logger.exception(e)
                            await message.channel.send(
                                "The server is overloaded or not ready yet."
                            )


async def setup(bot):
    await bot.add_cog(ChatbotCog(bot))
