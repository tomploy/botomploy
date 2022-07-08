import { Client, ClientOptions } from "discord.js";
import interactionCreate from "./listeners/interactionCreate";
import ready from "./listeners/ready";
require('dotenv').config();

const disc_tok = process.env.DISCORD_TOKEN; // add your token here

console.log("Bot is starting...");

const client = new Client({
    intents: []
});

ready(client);
interactionCreate(client);

client.login(disc_tok);

//	https://discord.com/api/oauth2/authorize?client_id=995062454377775115&permissions=146029177920&scope=bot%20applications.commands