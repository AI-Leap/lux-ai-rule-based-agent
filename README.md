# lux-ai-rule-based-agent

This agent is for Kaggle Competition, https://www.kaggle.com/c/lux-ai-2021

## Running the agent.
You need to install the npm package. https://www.npmjs.com/package/@lux-ai/2021-challenge
After installation, run `lux-ai-2021 main.py main.py`

This will output replay json. Afterwards, use this repo, https://github.com/Lux-AI-Challenge/Lux-Viewer-2021
to view the replay.

Overview Strategy

**Self-managed Clusters**
Cluster is king. The flow is

1. Cluster
2. Mission
3. Action

We will initialize the clusters.
The clusters will then decide the missions.
The workers will perform these missions.
Detailed discussion is written on Kaggle forum.
https://www.kaggle.com/c/lux-ai-2021/discussion/274436

## Code Structure
As a web developer, I use the project structure used for developing servers.
The classes, the controllers and the services.

We can call if microservice architectures.
Each service only knows and responsible for the class.
e.g., MissionService should only consists of mission related functions.

The controllers are for business logic consisting of interacting within services.
A controller can use more than one service.
The controllers are for algorithm step that requires coordination between services.

This code repository follows standard python linting and use pytest for test cases.
It has simple GitHub actions.

Feedbacks and Pull Requests are welcome.
