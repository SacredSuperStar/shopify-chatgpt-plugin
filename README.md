# Shopify Admin ChatGPT Plugin

An open source ChatGPT plugin for managing and asking questions about a Shopify store within ChatGPT.

## Shopify Setup

### Get an API Key for your Store from 

In order for this plugin to work, you will need to get an API key for your Shopify store. To do this, follow these steps:

1. Log in to your Shopify store.
1. Navigate to the Apps Settings page (in your store's Settings page).
1. Click the "Develop Apps" button in the top right. You may need to accept some conditions first before proceeding to the next step.
1. Click "Create an App"
1. Name it whatever you would like, for example: "ChatGPT Plugin"
1. Next, click "Configure Admin API Scopes" and select scopes. The minimum scopes required can be found [below](#shopify-scopes-used). Make sure you Save it.
1. Then, go to the "API Credentials" tab and click "Install app". This will generate an API token.
1. Finally, click "Reveal token once". **Make sure to copy this token and save it in a safe place.** You will need it later.


### Shopify Scopes Used

The following scopes are used by this plugin, or may be in the future:

- read_reports
- read_customers
- read_fulfillments
- read_inventory
- read_orders
- read_products
- read_checkouts
- read_content
- read_discounts
- read_draft_orders
- read_marketing_events
- read_price_rules
- read_product_listings
- read_publications
- read_shipping
- read_returns
- read_third_party_fulfillment_orders

Of course, feel free to add more scopes and update the APIs used as needed. This is just a minimal starting point.


## Testing Locally

If you'd like to test this plugin locally, follow these steps:

1. Install Python 3.10, if not already installed.
2. Clone the repository: `git clone https://github.com/acmeyer/shopify-admin-chatgpt-plugin.git`
3. Navigate to the cloned repository directory: `cd /path/to/shopify-admin-chatgpt-plugin`
4. Install poetry: `pip install poetry`
5. Create a new virtual environment with Python 3.10: `poetry env use python3.10`
6. Activate the virtual environment: `poetry shell`
7. Install app dependencies: `poetry install`
8. Set the required environment variables by copying `.env.example` file to `.env` and filling in the values.
9. Run the API locally: `poetry run start`
10. Access the API documentation at `http://0.0.0.0:8000/docs` and test the API endpoints.

**Note:** if you would like to make any changes to the local version of the plugin, you'll have to edit the files in the `local-server` directory. These are specifically placed for only local development for plugins.


## Testing the Plugin in ChatGPT

To test a plugin in ChatGPT, follow these steps:

1. Visit [ChatGPT](https://chat.openai.com/), select "Plugins" from the model picker, click on the plugins picker, and click on "Plugin store" at the bottom of the list.

1. Choose "Develop your own plugin" and enter the URL of the plugin (e.g. `localhost:8000` if testing locally, `https://<your-app-url>` if testing a deployed version) when prompted.

1. Your plugin is now enabled for your ChatGPT session.

**Note:** if testing a deployed version, you will need to provide a Bearer token. This should be the same Bearer token that you set in your Environment variables. This is just to add an extra layer of security, so that not just anyone can access your plugin and therefore your shop data.

For more information, refer to the [OpenAI documentation](https://platform.openai.com/docs/plugins/getting-started/openapi-definition).


## Deployment

There are a number of different ways you could deploy this application, however, for simplicity, this Readme explains how you can do it using either [Heroku](https://heroku.com) or [Fly.io](https://fly.io). Both are great options and should take minimal effort to get up and running. These instructions assume that you have at least signed up with one of these services first.

### General Deployment Setup

To deploy the Docker container from this repository to either Heroku or Fly.io, follow these steps:

[Install Docker](https://docs.docker.com/engine/install/) on your local machine if it is not already installed.

Clone the repository from GitHub:

```
git clone https://github.com/acmeyer/shopify-admin-chatgpt-plugin.git
```

Navigate to the cloned repository directory:

```
cd path/to/shopify-admin-chatgpt-plugin
```

**Hosting Specific Setups:**

- [Deploying to Heroku](#deploying-to-heroku)
- [Deploying to Fly.io](#deploying-to-flyio)


### Deploying to Heroku

Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) on your local machine.

Log in to the Heroku CLI:

```
heroku login
```

Create a Heroku app:

```
heroku create [app-name]
```

**IMPORTANT:** Update the Makefile and replace `<your app name>` with your actual app name.

Next, log in to the Heroku Container Registry by running:

```
make heroku-login
```

Build the Docker image using the Dockerfile and push it to the Heroku Container Registry by running:

```
make heroku-push
```

Set the required environment variables for your Heroku app:

```
heroku config:set SHOP_NAME=your_shop_name \
SHOP_API_KEY=your_shopify_api_key \
SHOP_DOMAIN_NAME=your-shop.myshopify.com \
BEARER_TOKEN=your_bearer_token \
HOST=https://<your app name>.herokuapp.com \
-a [app-name]
```

You could also set environment variables in the [Heroku Console](https://dashboard.heroku.com/apps).

After completing these steps, your Docker container should be deployed to Heroku and running with the necessary environment variables set.

You should now be able to find the OpenAPI schema at `<your_app_url>/.well-known/openapi.yaml` and the manifest at `<your_app_url>/.well-known/ai-plugin.json`.

**IMPORTANT:** Change the plugin url in your plugin manifest file [here](/.well-known/ai-plugin.json), and in your OpenAPI schema [here](/.well-known/openapi.yaml), to the url of your Heroku ap. This url will be `<your_app_url>`.

Redeploy the app by running: 

```
make heroku-push
```

To view your app logs, run:

```
heroku logs --tail -a [app-name]
```

### Deploying to Fly.io

Log in to the Fly.io CLI:

```
flyctl auth login
```

Create and launch your Fly.io app:

```
flyctl launch
```

Follow the instructions in your terminal:

- Choose your app name
- Choose your app region
- Don't add any databases
- Don't deploy yet (if you do, the first deploy might fail as the environment variables are not yet set)

Set the required environment variables:

```
flyctl secrets set SHOP_NAME=your_shop_name \
SHOP_API_KEY=your_shopify_api_key \
SHOP_DOMAIN_NAME=your-shop.myshopify.com \
BEARER_TOKEN=your_bearer_token \
HOST=https://<your app name>.fly.dev
```

Alternatively, you could set environment variables in the [Fly.io Console](https://fly.io/dashboard).

**IMPORTANT:** Change the plugin url in your plugin manifest file [here](/.well-known/ai-plugin.json), and in your OpenAPI schema [here](/.well-known/openapi.yaml), to the url for your Fly.io app. This url will be `https://<your-app-name>.fly.dev`.

Deploy your app with:

```
flyctl deploy
```

After completing these steps, your Docker container should be deployed to Fly.io and running with the necessary environment variables set. You can view your app by running:

```
flyctl open
```

which will open your app url. You should be able to find the OpenAPI schema at `<your_app_url>/.well-known/openapi.yaml` and the manifest at `<your_app_url>/.well-known/ai-plugin.json`.

To view your app logs:

```
flyctl logs
```

#### Debugging tips
Fly.io uses port 8080 by default.

If your app fails to deploy, check if the environment variables are set correctly, and then check if your port is configured correctly. You could also try using the [`-e` flag](https://fly.io/docs/flyctl/launch/) with the `flyctl launch` command to set the environment variables at launch.

## Fully Hosted Version

If there's enough interest, I can create a hosted version of this repository and make it a Shopify app and ChatGPT plugin. That would make it easier to use and you wouldn't have to worry about getting this all set up on your own. Plus, it would get updated with new features as they get added.

If you'd be interested in using something like this, please let me know and fill out this [form](https://forms.gle/NUdh4QgvvVGKr19x8).