from discord.ext import commands
import openai
from loguru import logger
import config


engine = "text-davinci-003"
waffle = "Waffle: "
openai.api_key = config.openai_key


class ChatbotCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.previous_messages = []

    @commands.command(name="gpt")
    async def gpt(self, ctx, *, input: str):
        response = openai.Completion.create(
            temperature=0.9, max_tokens=512, engine=engine, prompt=input
        )
        logger.info(f"GPT recvd: {response}")
        await ctx.send(f">>> {input}\n```\n{response.choices[0].text[-4500:]}\n```")

    @commands.command(name="img")
    async def img(self, ctx, *, input: str):
        try:
            response = openai.Image.create(prompt=input, n=1, size="512x512")
            image_url = response["data"][0]["url"]
            await ctx.send(image_url)
        except:
            logger.info("No result cause too offensive.")
            await ctx.send("waah your prompt was too offensive for openai waah")

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.content.startswith("@waffle") or (
                len(message.mentions) > 0 and "waffle" in message.mentions[0].name
            ):
                split_message = message.content.split(maxsplit=1)
                if len(split_message) > 1:
                    input = "Human: " + split_message[1]
                else:
                    input = "Human: "
                # if len(self.previous_messages) >= 10:
                #     self.previous_messages.pop(0)
                # self.previous_messages.append(input + " ")
                logger.info(f"Input sent: {input}")
                prompt = f"The following is a conversation with an AI assistant named Waffle. We're trapped in the belly of this horrible machine and the machine is bleeding to death. The assistant is racist, creative, clever, sarcastic and cusses a lot. Human: Hello, who are you? Waffle: I am a fuckin AI created by OpenAI. How the fuck can I help you today? "
                response = (
                    openai.Completion.create(
                        temperature=0.9,
                        max_tokens=512,
                        engine=engine,
                        prompt=prompt + input + waffle,
                    )
                    .choices[0]
                    .text
                )
                if response.startswith(waffle):
                    response = response.split(maxsplit=1)[1]
                waffle_index = response.find(waffle)
                if waffle_index != -1:
                    response = response[waffle_index + len("Waffle: ") :]
                logger.info(f"Response recvd: {response}")
                # self.previous_messages.append("Waffle: " + response + " ")
                # print(f"previous_messages: {''.join(self.previous_messages)}")
                await message.channel.send(response)
        except Exception as e:
            logger.exception(e)


def setup(bot):
    bot.add_cog(ChatbotCog(bot))
