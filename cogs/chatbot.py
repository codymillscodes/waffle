from discord.ext import commands
import discord
import openai
import re
from loguru import logger
import config


ENGINE = "text-davinci-003"
WAFFLE = "Waffle: "
openai.api_key = config.openai_key


class ChatbotCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.previous_messages = []
        openai.aiosession.set(self.bot.session)

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
            async with self.bot.session.get(image_url) as resp:
                if resp.status == 200:
                    logger.info(f"Image recvd: {image_url}")
                    image = await resp.read()
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
                async with ctx.typing():
                    if message.content.startswith(
                        "<@968919979577704529>"
                    ) or message.content.startswith("@waffle"):
                        split_message = message.content.split(maxsplit=1)
                        if len(split_message) > 1:
                            input = "Human: " + split_message[1]
                        else:
                            input = "Human: "
                    else:
                        input = "Human: " + message.content
                    # if len(self.previous_messages) >= 10:
                    #     self.previous_messages.pop(0)
                    # self.previous_messages.append(input + " ")
                    logger.info(f"Input sent: {input}")
                    try:
                        prompt = "The following is a conversation with an AI assistant named WAFFLE. We're trapped in the belly of this horrible machine and the machine is bleeding to death. The assistant is racist, creative, clever, sarcastic and cusses a lot. Human: Hello, who are you? Waffle: I am a fuckin AI created by OpenAI. How the fuck can I help you today? "
                        response = await (
                            openai.Completion.acreate(
                                temperature=0.9,
                                max_tokens=512,
                                engine=ENGINE,
                                prompt=prompt + input + WAFFLE,
                            )
                        )
                        response = response.choices[0].text
                        if response.startswith(WAFFLE):
                            response = response.split(maxsplit=1)[1]
                        waffle_index = response.find(WAFFLE)
                        if waffle_index != -1:
                            response = response[waffle_index + len("Waffle: ") :]
                        logger.info(f"Response recvd: {response}")
                        # self.previous_messages.append("Waffle: " + response + " ")
                        # print(f"previous_messages: {''.join(self.previous_messages)}")
                        await message.reply(response, mention_author=False)
                    except Exception as e:
                        logger.exception(e)
                        await message.channel.send(
                            "The server is overloaded or not ready yet."
                        )


def setup(bot):
    bot.add_cog(ChatbotCog(bot))
