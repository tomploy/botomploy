import { CommandInteraction, Client, MessageEmbed, TextChannel } from "discord.js";
import { blockQuote } from "@discordjs/builders";
import { Command } from "../Command";

export const Event: Command = {
    name: "event",
    description: "manage collective events",
    type: "CHAT_INPUT",
    options: [
        {
            "name": "new",
            "description": "créer un nouvel evenement",
            "type": 1,
            "options": [
                {
                    "name": "name",
                    "description": "Nom de l'évenement",
                    "type": 3,
                    "required": true
                },
                {
                    "name": "date",
                    "description": "Date de l'évenement",
                    "type": 3,
                    "required": true
                },
                {
                    "name": "description",
                    "description": "description de l'évenement",
                    "type": 3,
                    "required": true
                }
            ]
        },
        {
            "name": "poll",
            "description": "sondage pour une date",
            "type": 1
        }
    ],
    run: async (client: Client, interaction: CommandInteraction) => {

        switch (interaction.options.getSubcommand()) {
            case "new":
                const embed = new MessageEmbed()
                    .setTitle(interaction.options.getString("name")!)
                    .setDescription(interaction.options.getString("description")!)
                    .addField("Date", interaction.options.getString("date")!)
                    .addFields(
                        { name: "<:checkmark:995720930426900520> Disponible (0)", value: blockQuote(" \n \n \n"), inline: true },
                        { name: "<:crossmark:995720931420934286> Indisponible (0)", value: blockQuote(" \n \n \n"), inline: true },
                        { name: "<:questionmark:995720932456935454> Peut-être (0)", value: blockQuote(" \n \n \n"), inline: true },
                    );
                interaction.reply({
                    embeds: [embed],
                    fetchReply: true,
                }).then(async value => {
                    const channel = await client.channels.fetch(interaction.channelId) as TextChannel;
                    const msg = await channel.messages.fetch(value.id);
                    if (msg !== undefined) {
                        await msg.react("995720930426900520");
                        await msg.react("995720931420934286");
                        await msg.react("995720932456935454");
                    } else {
                        console.error("Impossible de fetch le message");
                    }
                });
                break;
            case "poll":
                break;
        }
    }
};