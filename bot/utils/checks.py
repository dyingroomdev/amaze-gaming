from discord.ext import commands

def is_mod_or_admin():
    """Check if the user has Moderator or Admin role or is server administrator."""
    async def predicate(ctx):
        mod_role_names = ["Moderator", "Admin"]  # Change these role names to your server's mod/admin roles
        author_roles = [role.name for role in ctx.author.roles]

        if any(role in mod_role_names for role in author_roles) or ctx.author.guild_permissions.administrator:
            return True
        return False
    return commands.check(predicate)

def is_admin():
    """Check if the user has Admin role or is server administrator."""
    async def predicate(ctx):
        admin_role_names = ["Admin"]  # Change to your server's admin role names
        author_roles = [role.name for role in ctx.author.roles]

        if any(role in admin_role_names for role in author_roles) or ctx.author.guild_permissions.administrator:
            return True
        return False
    return commands.check(predicate)

def is_mod():
    """Check if the user has Moderator role or is server administrator."""
    async def predicate(ctx):
        mod_role_names = ["Moderator"]  # Change to your server's mod role names
        author_roles = [role.name for role in ctx.author.roles]

        if any(role in mod_role_names for role in author_roles) or ctx.author.guild_permissions.administrator:
            return True
        return False
    return commands.check(predicate)
