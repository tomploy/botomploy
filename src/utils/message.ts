import { CacheType, Client, CommandInteraction, Message, TextChannel } from "discord.js";
import { APIMessage } from "discord-api-types/v9";

export async function getMessage(client: Client, interaction: CommandInteraction<CacheType>, message: Message<boolean>|APIMessage): Promise<Message<boolean>> {
    const channel = await client.channels.fetch(interaction.channelId) as TextChannel;
    return await channel.messages.fetch(message.id);
}