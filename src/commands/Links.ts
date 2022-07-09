import { BaseCommandInteraction, Client, MessageEmbed } from "discord.js";
import { Command } from "../Command";
import links from "../links.json"

interface Link {
    name: string;
    url: string;
}

export const Links: Command = {
    name: "links",
    description: "give important links",
    type: "CHAT_INPUT",
    run: async (client: Client, interaction: BaseCommandInteraction) => {
        
        const embed = new MessageEmbed()
            .setTitle("__L I N K S__")
            .setDescription("useful links related to the collective.")
            .addField("main hubs", getLinks(links.orga), true)
            .addField("ressources", getLinks(links.resources), true)


        await interaction.followUp({
            ephemeral: true,
            embeds: [embed]
        });
    }
};

function getLinks(arr: Link[]): string {
    let links: string = ""; 
    arr.forEach(element => {
        links += "- [" + element.name + "](" + element.url + ") \n";
    });
    return links;
}
