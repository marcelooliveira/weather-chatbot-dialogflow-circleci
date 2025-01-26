---
layout: post
featured: false
popular: false
date: '2020-04-02 9:00'
published: true
title: Test title
author: ron-powell
image: /blog/media/Tutorial-Intermediate.jpg
html_title: >-
  Test title | CircleCI
description: >-
  Test description
summary: >-
  Same as test description
tags:
  - tutorials
  - engineering
pinned: false
---

This test post also serves as a guide for the writing in markdown and some conventions we use.

## Titles

## Use this for section titles

_In Markdown_:

```markdown
## Use this for section titles
```

Use `sentence-case` for titles and headers.

## Terminal commands

```bash
npm init -y
```

_In Markdown_:

  ```markdown
    ```bash
    npm init -y
    ```
  ```

## Code snippets

If the text preceding a code snippet suggests that you copy the code, use a `colon` signifying this. Use a period if you are just describing the code.

### Example

> The following is an excerpt from a blog post. Note the use of a full stop instead of a colon.

You can specify the name, theme and background colors in the manifest file for your app. Below is a snippet of my `manifest.json`.

```json
{
  "name": "my-awesome-app",
  "theme_color": "#000000",
  "background_color": "#ffffff",
}
```

## Included image

> Using markdown

![alt text for image2](../src/blog/media/2020-04-15-image2.jpg)

_In Markdown_:

```markdown
![alt text for image2](../src/blog/media/2020-04-15-image2.jpg)
```

> Using HTML

<div style="text-align:center"><img alt="alt text for image" src="../src/blog/media/2020-04-15-image2.jpg"/></div>

_In Markdown_:

```markdown
<div style="text-align:center"><img alt="alt text for image" src="../src/blog/media/2020-04-15-image2.jpg"/></div>
```

Do not use a colon leading up to an image.

## Other texts

## Links

Linked text example: [CircleCI blog][1]

_In Markdown_:

```markdown
Linked text example: [CircleCI blog][1]
...

// at the end of the file
[1]: https://circleci.com/blog/
```

_OR_:

```markdown
Linked text example: [CircleCI blog](https://circleci.com/blog/)
```

## Important to note

**Note**: <i>Some important information</i>

_In Markdown_:

```markdown
**Note**: <i>Some important information</i>
```

## Listing items

Use the Oxford comma.

```txt
You will need a pencil, paper, and ruler.
```

The Oxford comma is the one that comes after "paper". The Oxford comma is also called the serial comma.

Refer to this [Markdown guide][guide] for more on the Markdown syntax.

[1]: https://circleci.com/blog/
[guide]: https://www.markdownguide.org/










# Title: Building a Chatbot with Dialogflow And CircleCI

Here we'll guide users on building a conversational chatbot app and deploying it to Azure Function app written in Python. The chatbot app will interact with using Google Dialogflow and https://openweathermap.org to answer user questions related to current weather data in specific world location. Topics to be covered: designing conversation flows, integrating with external APIs, and use CircleCI to set up a CI/CD pipeline for continuous integration and deployment of chatbot updates. We'll use CircleCI to deploy our code to Azure Function app every time our GitHub repo is updated. In the end, users will be able to pass questions to Azure Function app and receive weather prediction answers produced by the chatbot.

### **Outline for the Tutorial: Building a Chatbot with Dialogflow and CircleCI**

---

## **Introduction (200 words)**  
- **Purpose of the tutorial**: Guide users in building a weather-related conversational chatbot app using Python, deploying it to Azure Function Apps, and managing updates with CircleCI.  
- **Key components involved**:  
  - **Dialogflow**: Designing conversation flows and natural language understanding.  
  - **OpenWeatherMap API**: Fetching real-time weather data.  
  - **CircleCI**: Automating CI/CD for streamlined updates.  
- **Expected outcomes**: By the end, users will have a fully functional chatbot capable of answering weather-related questions in specific locations and continuously updated through a robust deployment pipeline.  

---

## **Prerequisites (100 words)**  
- **Knowledge prerequisites**:  
  - Basic Python programming.  
  - Familiarity with REST APIs.  
  - Understanding of CI/CD principles.  
- **Tools and accounts required**:  
  - Python 3.8+ installed locally.  
  - Azure account with Function App setup.  
  - Dialogflow account for chatbot development.  
  - OpenWeatherMap API key.  
  - GitHub account and basic repository knowledge.  
  - CircleCI account connected to GitHub.  

---

## **Body (1000 words)**  

### **1. Designing the Chatbot with Dialogflow**  
- **Overview of Dialogflow**:  
  - Key components: intents, entities, and fulfillment.  
- **Creating the Dialogflow agent**:  
  - Step-by-step process: agent creation, configuring intents, and defining user utterances.  
- **Customizing responses**:  
  - Static vs. dynamic responses using fulfillment.

#### agent creation

Let's create an agent named WeatherBot...

#### configuring intents

Let's create the intents inside the WeatherBot agent, by following the steps belows:

---

### **Step 1: Set Up the Dialogflow Project**
1. Log in to the [Dialogflow Console](https://dialogflow.cloud.google.com/).
2. Open or create the project where you will create the intents.

---

### **Step 2: Create Intents**
#### **1. Create the `Greeting` Intent**
1. Navigate to **Intents** in the left menu.
2. Click **+ Create Intent** and name it `Greeting`.
3. **Training Phrases**:
   - Add the greeting phrases: "Hi" and "Hello".
4. **Responses**:
   - Add the Text Response: `"Hello! I'm a weather bot. Do you have the precise coordinates of the location you want to know the weather for?"`.
5. Save the intent.

---

#### **2. Create the `Yes_Coordinates Flow` Intent**
1. In the /intents page of your agent in DialogFlow, move the mouse over the Greeting intent and click the **Add follow-up intent** link, then choose the **yes** option.
2. Open the created intent and rename it as `Yes/Coordinates Flow`.
3. **Responses**:
   - Add responses such as `"Enter the standard latitude and longitude format, which for New York City, for example, would be: 40°42′46″N 74°0′22″W."`.
4. Save the intent.

---

#### **3. Create the `GetWeatherByCoordinates` Intent**
1. In the /intents page of your agent in DialogFlow, move the mouse over the "Yes/Coordinates Flow" intent and click the **Add follow-up intent** link, then choose the **custom** option.
2. Open the created intent and rename it as `GetWeatherByCoordinates`.
3. **Responses**:
   - Check the "Set this intent as end of conversation" option.
4. **Fullfilment**:
   - Set the Enable webhook call for this intent as `true`.
5. Save the intent.

---

#### **4. Create the `No/City Flow` Intent**
1. In the /intents page of your agent in DialogFlow, move the mouse over the Greeting intent and click the **Add follow-up intent** link, then choose the **no** option.
2. Open the created intent and rename it as `No/City Flow`.
3. **Responses**:
   - Add the Text Response: `"Enter the city name."`.
4. Save the intent.

---

#### **5. Create the `GetCityName` Intent**
1. In the /intents page of your agent in DialogFlow, move the mouse over the "No/City Flow" intent and click the **Add follow-up intent** link, then choose the **custom** option.
2. Open the created intent and rename it as `GetCityName`.
3. **Training Phrases**:
   - Add the training phrases: "New York" and "Tokyo".
4. **Parameters**:
   - Make sure the parameter below has been created by the training phrases:
     - **Name:** `geo-city`, **Entity:** `@sys.geo-city`, **Required:** Yes.
6. **Responses**:
   - Add the Text Response: `"Enter the state/province name."`.
7. Save the intent.

---

#### **6. Create the `GetStateName` Intent**
1. In the /intents page of your agent in DialogFlow, move the mouse over the "GetCityName" intent and click the **Add follow-up intent** link, then choose the **custom** option.
2. Open the created intent and rename it as `GetStateName`.
3. **Training Phrases**:
   - Add the training phrases: "California" and "Chihuahua".
4. **Parameters**:
   - Make sure the parameter below has been created by the training phrases:
     - **Name:** `geo-state`, **Entity:** `@sys.geo-state`, **Required:** Yes.
5. **Responses**:
   - Add Text Response: `"Enter the country name."`.
6. Save the intent.

---

#### **7. Create the `GetCountryName` Intent**
1. In the /intents page of your agent in DialogFlow, move the mouse over the "GetStateName" intent and click the **Add follow-up intent** link, then choose the **custom** option.
2. Open the created intent and rename it as `GetCountryName`.
3. **Parameters**:
   - Make sure the parameter below has been created by the training phrases:
     - **Name:** `geo-country`, **Entity:** `@sys.geo-country`, **Required:** Yes.
4. **Responses**:
   - Check the "Set this intent as end of conversation" option.
5. **Fullfilment**:
   - Set the Enable webhook call for this intent as `true`.
6. Save the intent.

---

### **Step 5: Deploy**
1. Integrate the bot with a platform (e.g., a website or messaging app).
2. Monitor interactions and fine-tune as needed.

This step-by-step guide ensures the flow aligns with the sequence provided.

### **2. Integrating with the OpenWeatherMap API**  
- **Setting up OpenWeatherMap**:  
  - Obtaining the API key.  
  - Understanding API documentation and query parameters.  
- **Writing Python scripts for API integration**:  
  - Fetching current weather data for user-specified locations.  
  - Formatting and error handling for API responses.  

### **3. Deploying the Chatbot to Azure Function App**  
- **Setting up Azure Function App**:  
  - Configuring a Python Function App.  
  - Understanding function triggers for HTTP-based interactions.  
- **Deploying the chatbot code**:  
  - Packaging Python dependencies using `requirements.txt`.  
  - Testing deployment with Azure Function App’s tools.  

### **4. Setting Up CI/CD with CircleCI**  
- **Overview of CircleCI and its role in deployment**.  
- **Configuring CircleCI for the project**:  
  - Creating the `config.yml` file.  
  - Setting up build, test, and deploy workflows.  

az login --tenant [YOUR-AZURE-TENANT]
az group create --name [YOUR-AZURE-RESOURCE-GROUP] --location [YOUR-AZURE-REGION]
az ad sp create-for-rbac --name circleci-weather-sp --role Contributor --scopes /subscriptions/[YOUR-AZURE-SUBSCRIPTION]/resourceGroups/[YOUR-AZURE-RESOURCE-GROUP]
az storage account create --name circleciweatherstorage --location [YOUR-AZURE-REGION] --resource-group [YOUR-AZURE-RESOURCE-GROUP] --sku Standard_LRS
az functionapp create --resource-group [YOUR-AZURE-RESOURCE-GROUP] --consumption-plan-location [YOUR-AZURE-REGION] --runtime python --runtime-version "3.11" --functions-version 4 --name circleci-weather-functionapp --os-type linux --storage-account circleciweatherstorage


- **Connecting CircleCI to GitHub and Azure**:  
  - Setting up GitHub triggers for CircleCI.  
  - Configuring Azure credentials in CircleCI for deployment.  

- When setting up the CI pipeline, be sure to walk through the config, explaining what's happening in different jobs and steps. Assume the reader might not know much (or anything) about CI/CD. Showcase the value and provide a practical demonstration of the setup.
- No hard sell, just walk folks through what's happening and why it's beneficial as they probably aren't familiar, and we want to give them reason to sign up for free.

### **5. Testing and Validating the Chatbot**  
- **Testing conversation flows in Dialogflow**:  
  - Using the built-in simulator.  
- **Testing API integrations**:  
  - Debugging responses from OpenWeatherMap.  
- **Validating the deployment pipeline**:  
  - Triggering a sample deployment via CircleCI. End by demonstrating a simple update to the app that triggers the pipeline. Bonus points if you can show the pipeline catching an error, then making a quick fix and the pipeline building green. 

### **Step 3: Test the Coordinates Flow**
1. Use the **Try it now** panel in the Dialogflow console.
2. Type in 'Hi' in the **Try it now** field.
3. DialogFlow will respond with "Hello! I'm a weather bot. Do you have the precise coordinates of the location you want to know the weather for?"
4. Type in 'Yes' in the **Try it now** field.
5. DialogFlow will respond with "Enter the standard latitude and longitude format, which for New York City, for example, would be: 40°42′46″N 74°0′22″W."
6. Type in '40°42′46″N 74°0′22″W' in the **Try it now** field.
7. DialogFlow will respond with something like "The weather for lat 40.71 lon -74.01 is few clouds with a temperature of 5.68ºC.".

---

### **Step 4: Test the City Name Flow**
1. Use the **Try it now** panel in the Dialogflow console.
2. Type in 'Hi' in the **Try it now** field.
3. DialogFlow will respond with "Hello! I'm a weather bot. Do you have the precise coordinates of the location you want to know the weather for?"
4. Type in 'No' in the **Try it now** field.
5. DialogFlow will respond with "Enter the city name."
6. Type in 'Munich' in the **Try it now** field.
7. DialogFlow will respond with "Enter the state/province name."
8. Type in 'Bavaria' in the **Try it now** field.
9. DialogFlow will respond with "Enter the country name."
10. Type in 'Germany' in the **Try it now** field.
11. DialogFlow will respond with "The weather for Munich / Bavaria / Germany is overcast clouds with a temperature of 1.94ºC."

---

## **Conclusion (300 words)**  
- **Summary of the process**:  
  - Designed a weather chatbot with Dialogflow.  
  - Integrated OpenWeatherMap for real-time data.  
  - Deployed the chatbot to Azure Functions using CircleCI for CI/CD.
  - Set up the Azure Function app so that users receive weather prediction answers produced by the chatbot.
- **Key takeaways**:  
  - Combining cloud services like Azure and Dialogflow enables scalable chatbot applications.  
  - CI/CD with CircleCI ensures continuous updates and smooth deployment.  
- **Future possibilities**:  
  - Enhancing chatbot capabilities with more APIs (e.g., location-based services).  
  - Using advanced AI features in Dialogflow or Azure Cognitive Services.  
- **Encouragement for exploration**: Links to official documentation for Azure Functions, Dialogflow, OpenWeatherMap, and CircleCI for further learning.  
