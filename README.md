# How to


# Docs

```
# to fix generated file for editing do sudo chmod -R 777 docs/*

docker-compose -f docs/docker-compose.yml build

# clean
# sudo rm -rd docs/build

# generate terraform doc
# sudo rm infrastructure/terraform/backend/DOC-Terraform.md
# sudo rm infrastructure/terraform/frontend/DOC-Terraform.md
docker-compose -f docs/docker-compose.yml run sphinx terraform-docs markdown table --output-file DOC-Terraform.md --output-mode inject ../infrastructure/terraform/frontend/
docker-compose -f docs/docker-compose.yml run sphinx terraform-docs markdown table --output-file DOC-Terraform.md --output-mode inject ../infrastructure/terraform/backend/

# generate backend code doc
# sudo rm -rf docs/source/code
docker-compose -f docs/docker-compose.yml run sphinx sphinx-apidoc -o source/code ../backend

# generate db doc
# sudo rm -rf docs/source/_static/db.png
docker-compose -f docs/docker-compose.yml run sphinx ../backend/manage.py graph_models --pydot -a -g -o source/_static/db.png

# generate statics and run server
docker-compose -f docs/docker-compose.yml run sphinx make html
docker-compose -f docs/docker-compose.yml up
# open browser at localhost:9001
```

# Telegram

## How to create a bot

**Step 1.** Enter @Botfather in the search tab and choose this bot.
![img1](assets/img1.webp)
Click “Start” to activate BotFather bot.
![img2](assets/img2.webp)
In response, you receive a list of commands to manage bots.

**Step 2**. Choose or type the `/newbot` command and send it.
![img3](assets/img3.webp)
**Step 3.** Choose a name for your bot — your subscribers will see it in the conversation. And choose a username for your bot — the bot can be found by its username in searches. The username must be unique and end with the word “bot.”
![img4](assets/img4.webp)
After you choose a suitable name for your bot — the bot is created. You will receive a message with a link to your bot t.me/<bot_username>, recommendations to set up a profile picture, description, and a list of commands to manage your new bot.

To connect a bot you need a token. Copy your token value and find more information about connecting your bot in the next steps.
![img5](assets/img5.webp)

## How to connect your bot

You can set up your webhook connection by calling this API pasting your bot token and setting the url of your server

```BASH
curl --request GET \
  --url 'https://api.telegram.org/<token>/setWebhook?url=<url>/telegram'
```
