import discord
from botomploy.utils.emojis import emojis_db

empty_choice = "n o b o d y"
class PollData():
    def __init__(self, title, items, emojis, desc = ""):
        self.message = None;
        self.title = title;
        self.choices = []
        self.embed = discord.Embed(
            title=title,
            color=discord.Color.purple(),
            description=desc
        )
        self.emojis = emojis_db[emojis]

        for i in range(len(items)):
            item_dict = {
                "item": items[i],
                "members": []
            }
            self.choices.append(item_dict)
            self.embed.add_field(name=str(self.emojis[i]) + " " + self.choices[i]["item"], value=empty_choice, inline=True)

    async def add_reactions(self, message):
        self.message = message
        for i in range(len(self.choices)):
            await self.message.add_reaction(self.emojis[i])
    
    def add_member(self, emoji, member):
        index = self.emojis.index(emoji)
        field = self.embed.fields[index]
        self.choices[index]["members"].append(member)

        value = ""
        for member in self.choices[index]["members"]:
            value += f"<@!{member}>\n"
            # value += ">>> <@!{}>\n".format(member)
        field.value = value;

    def remove_member(self, emoji, member):
        index = self.emojis.index(emoji)
        field = self.embed.fields[index]
        self.choices[index]["members"].remove(member)

        value = ""
        for member in self.choices[index]["members"]:
            value += f"<@!{member}>\n"

        field.value = value if len(self.choices[index]["members"]) > 0 else empty_choice;
    
    