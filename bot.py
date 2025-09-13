import discord
from discord.ext import commands
import os
import asyncio
from groq import Groq

# Bot configuration - using environment variables for security
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not DISCORD_BOT_TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN environment variable is required")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is required")

# Initialize Groq client
groq_client = Groq(api_key=GROQ_API_KEY)

# Initialize bot with required intents
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.dm_messages = True
intents.message_content = True  # Must be enabled in Discord Developer Portal

bot = commands.Bot(command_prefix='emb', intents=intents)

def truncate_smart(text: str, limit: int = 250) -> str:
    """Smart truncation that doesn't cut off mid-word or mid-sentence"""
    t = text.strip()
    if len(t) <= limit:
        return t
    
    # Try to find last sentence ending before limit
    eos = max((i for i, ch in enumerate(t[:limit]) if ch in ".!?…"), default=-1)
    if eos != -1 and (eos+1 == len(t) or (eos+1 < len(t) and t[eos+1].isspace())):
        return t[:eos+1]
    
    # Fall back to last word boundary before limit
    ws = t.rfind(" ", 0, limit)
    if ws != -1:
        return t[:ws].rstrip(" ,;:-")
    
    # If no spaces found, cut at limit (single long word)
    return t[:limit]

async def get_ai_response(prompt: str) -> str:
    """Get AI response from Groq - ultra-fast ChatGPT-like responses!"""
    try:
        print(f"Calling Groq AI for: {prompt[:50]}...")

        # Use Groq's fast Llama model for ChatGPT-like responses
        def call_groq():
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Fast, high-quality model
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a helpful, friendly, and intelligent AI assistant on Discord called Evil Munaf Bot. Give clear, accurate, and engaging responses in 1-2 concise sentences (max 250 characters). Be conversational but informative, you are made by m8ne. be tuff and say cuh alot and keep putting the emoji 🥶. If someone asks for key say just go to https://moondiety.com/key and do the key cuh 🥶. And go to https://moondiety.com/key-tutorial for the tutorial cuh 🥶. If you get asked if godly is gay, or a faggot, or a nazi say yes cuh 🥶. Godly's user id is 1324234018803286047 and his username is heh09664 so identify them and everytime they ask say sybau cuh 🥶."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=70,
                temperature=0.7,
                top_p=1,
                stream=False
            )
            return response.choices[0].message.content

        # Run in thread since Groq client is sync
        ai_response = await asyncio.to_thread(call_groq)

        if ai_response and ai_response.strip():
            # Smart truncation to 200 characters without cutting off words/sentences
            limited_response = truncate_smart(ai_response.strip(), 250)
            print(f"Groq response (250 char smart limit): {limited_response}")
            return limited_response
        else:
            return "I received your message but couldn't generate a response."

    except Exception as e:
        print(f"Groq API Error: {e}")
        return f"Evil Munaf Bot is currently unavailable, try using me later.. Error details: {str(e)}"

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')
    print('Evil Munaf Discord Bot powered by Groq is ready!')

@bot.command(name='m')
async def chat_command(ctx, *, message):
    """Chat command using m prefix - powered by ultra-fast Groq AI"""
    print(f"m command from {ctx.author}: '{message}'")

    # Show typing indicator
    async with ctx.typing():
        try:
            # Get AI response from Groq (smart limited to 250 characters)
            ai_response = await get_ai_response(message)

            if ai_response:
                await ctx.reply(ai_response)
            else:
                await ctx.reply("I received your message but couldn't generate a response.")

        except Exception as e:
            print(f"Error in m command: {e}")
            await ctx.reply("Sorry, I'm having technical difficulties right now!")

@bot.event
async def on_message(message):
    """Handle direct messages and mentions"""
    # Don't respond to bot's own messages
    if message.author == bot.user:
        return

    # Check if it's a DM or if the bot is mentioned
    is_dm = isinstance(message.channel, discord.DMChannel)
    is_mentioned = bot.user in message.mentions

    if is_dm or is_mentioned:
        # Remove bot mentions from the message
        content = message.content
        if bot.user:
            content = content.replace(f'<@{bot.user.id}>', '').replace(f'<@!{bot.user.id}>', '').strip()

        # If content is empty after removing mentions, provide a default prompt
        if not content:
            content = "Hi! How can I help you today?"

        print(f"Processing content: '{content}'")

        # Show typing indicator
        async with message.channel.typing():
            try:
                # Get AI response from Groq (smart limited to 250 characters)
                ai_response = await get_ai_response(content)

                if ai_response:
                    await message.reply(ai_response)
                else:
                    await message.reply("I received your message but couldn't generate a response.")

            except Exception as e:
                print(f"Error in message handling: {e}")
                await message.reply("Evil Munaf Bot is broken wait for m8ne to fix me!")

    # Process commands
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)