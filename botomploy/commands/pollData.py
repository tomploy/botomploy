import discord
from botomploy.utils.emojis import emojis

empty_choice = "n o b o d y"
class PollData():
    def __init__(self, title, items, emoji_type, desc = ""):
        self.message_id = None
        self.title = title
        self.choices = []
        self.desc = desc
        self.emoji_type = emoji_type

        for i in range(len(items)):
            item_dict = {
                "item": items[i],
                "members": []
            }
            self.choices.append(item_dict)
    
    def add_member(self, emoji, member):
        index = emojis[self.emoji_type].index(emoji)
        self.choices[index]["members"].append(member)

    def remove_member(self, emoji, member):
        index = emojis[self.emoji_type].index(emoji)
        self.choices[index]["members"].remove(member)

    def embed(self):
        embed = discord.Embed(
            title=self.title,
            color=discord.Color.purple(),
            description=self.desc
        )

        i = 0
        for choices in self.choices:
            name = str(emojis[self.emoji_type][i]) + " " + choices["item"]
            embed.add_field(name=name, value="n o b o d y", inline=True)

            value = ""  
            for member in choices["members"]:
                value += f"<@!{member}>\n"
                # value += ">>> <@!{}>\n".format(member)
                embed.fields[i].value = value
            i += 1
        return embed 
