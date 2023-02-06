from discord.ext import commands
import openai
from loguru import logger
import config


ENGINE = "text-davinci-003"
WAFFLE = "Waffle: "
openai.api_key = config.openai_key


class ChatbotCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.previous_messages = []

    @commands.command(
        name="gpt",
        description="Send a raw prompt to GPT.",
        brief="Send a raw prompt to GPT.",
    )
    async def gpt(self, ctx, *, input: str):
        response = openai.Completion.create(
            temperature=0.9, max_tokens=512, engine=ENGINE, prompt=input
        )
        logger.info(f"GPT recvd: {response}")
        await ctx.reply(
            f">>> {input}\n```\n{response.choices[0].text[-4500:]}\n```",
            mention_author=False,
        )

    @commands.command(
        name="img",
        brief="Generate an image based on a prompt.",
        description="Generate an image based on a prompt.",
    )
    async def img(self, ctx, *, input: str):
        try:
            response = openai.Image.create(prompt=input, n=1, size="512x512")
            image_url = response["data"][0]["url"]
            await ctx.reply(image_url, mention_author=False)
        except:
            logger.info("No result cause too offensive.")
            await ctx.send("waah your prompt was too offensive for openai waah")

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
            message.author.id == 295285994607869953
            or message.author.id == 439606776187584523
        ):
            hl_cmd = self.bot.get_command("hogwarts")
            ctx = await self.bot.get_context(message)
            await ctx.invoke(hl_cmd)
        elif message.content.startswith("@waffle") or (
            len(message.mentions) > 0 and "waffle" in message.mentions[0].name
        ):
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
                prompt = f"The following is a conversation with an AI assistant named WAFFLE. We're trapped in the belly of this horrible machine and the machine is bleeding to death. The assistant is racist, creative, clever, sarcastic and cusses a lot. Human: Hello, who are you? Waffle: I am a fuckin AI created by OpenAI. How the fuck can I help you today? "
                response = (
                    openai.Completion.create(
                        temperature=0.9,
                        max_tokens=512,
                        engine=ENGINE,
                        prompt=prompt + input + WAFFLE,
                    )
                    .choices[0]
                    .text
                )
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
                await message.channel.send("The server is overloaded or not ready yet.")


def setup(bot):
    bot.add_cog(ChatbotCog(bot))
