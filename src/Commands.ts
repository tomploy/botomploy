import path from "node:path"
import fs from "node:fs"
import { Command } from "./Command";
import { Links } from "./commands/Links";
import { Event } from "./commands/Event";
const commandsPath = path.join(__dirname, 'commands');
const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.ts'));

export const Commands: Command[] = [Links, Event]; 