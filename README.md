This repo is a collection of small Discord bots I have done. Here they are, in orderly fashion:
# Melanculator
> "para de reagir melancia em tudo mano"

A selfbot born out of an inside joke.
Annoy the hell out of your friends by reacting to every single message with emojis. 
## Running
Set the environment variables:
```ini
SELF_TOKEN=<token>
```
## Commands
*param -> optional
- `emoji <emoji*s>` - what emoji(s) to react, space separated 
- `assign <*chat id>` - react to single chat ONLY
- `append <*chat id>` - add channel to target list
- `remove <chat id>` - remove channel from target list
- `server` - add all of current server's channels to target list
- `reset` - empty target list
- `undercover <*f/t>` - delete command messages upon sending them
- `stop` - ..stop?
- `help` - show help dialog
## Note
- I did not create this with the intent of spamming or annoying anybody else except your close friends. Use with caution.
- You should input your own `SELF_TOKEN` in a `.env` file.
# Le Minecraft Bot
This WAS going to be an interface for local Minecraft servers, where you and your friends are able to control and log the state of your server from the convenience of Discord.
The development was halted because I faced some problems I'd never come across back then (mostly relating to input and output buffers).
May get back to finishing it if someone places a bet worth winning.