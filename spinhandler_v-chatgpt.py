import openai
import discord

# Set OpenAI API key
openai.api_key = "xx"

# Set Discord bot token
TOKEN = "xx"

# Initialize Discord client
client = discord.Client(intents=discord.Intents.all())


async def spin_text(prompt: str) -> str:
    """Use OpenAI's GPT-3 to spin the provided text.

    Arguments:
    prompt -- the text to spin

    Returns:
    The spun text
    """
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,

    )

    message = completions.choices[0].text
    return message


@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    if message.content.startswith("!spin"):
        # Extract the text to spin from the message
        text_to_spin = message.content[6:]

        # Spin the text
        spun_text = await spin_text(text_to_spin)

        # Send the spun text back to the channel
        await message.channel.send(spun_text)


client.run(TOKEN)
