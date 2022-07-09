import { BaseCommandInteraction, Client, MessageEmbed } from "discord.js";
import { Command } from "../Command";

export const Event: Command = {
    name: "event",
    description: "manage collective events",
    type: "CHAT_INPUT",
    options: [
        {
            "name" : "new",
            "description" : "truc",
            "type" : 3,
        },
        {
            "name" : "poll",
            "description" : "sondage pour une date",
            "type" : 3
        }
    ],
    run: async (client: Client, interaction: BaseCommandInteraction) => {
        
        const embed = new MessageEmbed()

        await interaction.followUp({
            ephemeral: true,
            embeds: [embed]
        });
    }
};