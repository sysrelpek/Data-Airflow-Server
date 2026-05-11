# scripts/grok_feedback_bot.py
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.command()
async def apply_fix(ctx, filename: str, content: str):
    """Körs när Grok eller du vill applicera en fix."""
    # Spara den nya YAML-filen i config/workflows/
    path = f"config/workflows/{filename}.yaml"
    with open(path, "w") as f:
        f.write(content)

    await ctx.send(f"✅ Fix applicerad på `{filename}.yaml`. Startar om build_manifest...")
    # Här kan du trigga build_manifest.py automatiskt
