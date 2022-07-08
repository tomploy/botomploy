import { Client, ClientOptions } from "discord.js";
import interactionCreate from "./listeners/interactionCreate";
import ready from "./listeners/ready";

const token = "OTk1MDYyNDU0Mzc3Nzc1MTE1.Gu0mag.Xr1j9kxAXlzPRqSQ5-v8U0VpfC6kL5MICCg24c"; // add your token here

console.log("Bot is starting...");

const client = new Client({
    intents: []
});

ready(client);
interactionCreate(client);

client.login(token);

//	https://discord.com/api/oauth2/authorize?client_id=995062454377775115&permissions=146029177920&scope=bot%20applications.commands