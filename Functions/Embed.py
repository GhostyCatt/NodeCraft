from datetime import datetime
import nextcord

async def Success(text:str) -> nextcord.Embed:
    """
    Success Embed
    -------------
    
    Input: `Text`
    
    Output: `nextcord.Embed` object
    """
    # Start constructing the embed
    embed = nextcord.Embed(
        title = "Success!",

        description = text,

        color = nextcord.Colour.red(),

        timestamp = datetime.utcnow()
    )
    # Return the embed
    return embed

async def Success(text:str) -> nextcord.Embed:
    """
    Success Embed
    -------------
    
    Input: `Text`
    
    Output: `nextcord.Embed` object
    """
    # Start constructing the embed
    embed = nextcord.Embed(
        title = "[ ■ ] Success",
        description = text,
        color = nextcord.Colour.red(),
        timestamp = datetime.utcnow()
    )
    # Return the embed
    return embed

async def Fail(text:str) -> nextcord.Embed:
    """
    Fail Embed
    -------------
    
    Input: `Text`
    
    Output: `nextcord.Embed` object
    """
    # Start constructing the embed
    embed = nextcord.Embed(
        title = "[ ■ ] Error",
        description = text,
        color = nextcord.Colour.red(),
        timestamp = datetime.utcnow()
    )
    # Return the embed
    return embed

async def Custom(title:str, text:str) -> nextcord.Embed:
    """
    Success Embed
    -------------
    
    Input: `Text`
    
    Output: `nextcord.Embed` object
    """
    # Start constructing the embed
    embed = nextcord.Embed(
        title = f"[ ■ ] {title}",
        description = text,
        color = nextcord.Colour.red(),
        timestamp = datetime.utcnow()
    )
    # Return the embed
    return embed