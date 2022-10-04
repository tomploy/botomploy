const { SlashCommandBuilder } = require("discord.js");
const { ActionRowBuilder, ButtonBuilder } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
        .setName("event")
        .setDescription("manage collective events"),
    async execute(interaction) {
        const row = new ActionRowBuilder()
            .addComponents(
                new ButtonBuilder()
                    .setCustomId('event')
                    .setLabel('event'),
                new ButtonBuilder()
                    .setCustomId('reunion')
                    .setLabel('reunion')
            );
        await interaction.reply({ components: [row] });
    }
        
}