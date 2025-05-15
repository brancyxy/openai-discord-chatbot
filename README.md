# Simple OpenAI powered discord chatbot
## Why?
Why not
## How do I use it?
Create an .env file with the following (or just load them into environment variables, should work):
```
DISCORD_TOKEN=<discord bot token here>
OPENAI_API_TOKEN=<openai token here>
```
You need the following dependencies, and if something's going wrong, these are the versions I used:
- Python (duh) (3.13)
- openai (1.78.1)
- nextcord (1.1.0)
- python-dotenv (1.1.0)

(And their dependencies too, of course)

#### Why not just provide dependencies.txt?
`Don't ask difficult questions`

Then just run `main.py`
- You can get the bot to reply to you when you say its username or tag it
- The ***/chat*** command forces the bot to respond.

Few features:
- It's primarily configured to run with the [Dreamgen](https://dreamgen.com/app) api, but you should be able to configure the AI backend in `config.ini` for any OpenAI interface with little to no changes needed.
- You can set the system prompt in... you wouldn't guess it... the `system_prompt.txt` file

## Will you even keep this updated
idk

## At least can I do it
Feel free to open a PR, I'll tentatively review it based on the size of it and my mood to so do, multiplied by the grade of me remembering this repo by that time.

##### Not affiliated with anyone, yada yada.