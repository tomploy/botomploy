import { Client } from "discord.js";
import interactionCreate from "./listeners/interactionCreate";
import ready from "./listeners/ready";
import * as dotenv from 'dotenv';
dotenv.config()

console.log("Bot is starting...");

const client = new Client({
    intents: []
});

ready(client);
interactionCreate(client);

client.login(process.env.DISCORD_TOKEN);

//	https://discord.com/api/oauth2/authorize?client_id=995062454377775115&permissions=146029177920&scope=bot%20applications.commands