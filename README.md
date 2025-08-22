# DownForAcross Discord Bot
discord bot that sends downforacross crossword puzzle links :) 

## Commands
- pingme
- puzzle (publisher)

## To Run Locally
### .env file 
Containing:
- `DISCORD_TOKEN`, the bot token
- `SERVER_IDS`, a comma separated list of serverIDs you'd like the bot to quickly update on when you make changes
- `TEST_SERVER_ID`, a serverID of a server for bot testing for the unfinished commands
- `PUZZLE_ROLE`, the name of a role in the server that gets pinged when a puzzle is sent

### OAuth2 Settings
Scopes:
- bot
- applications.commands (for slash commands)

Bot Permissions:
- Manage Roles (to add users to pinged puzzle role)
- Send Messages
- Embed Links
- Read Message History
- Use External Emojis
- Add Reactions
- Use Slash Commands
- Use Embedded Activities