# Microsoft Fabric CI/CD Demo

## Introduction
This repository demonstrates continuous integration and continuous deployment (CI/CD) workflows for Microsoft Fabric artifacts. 
It showcases how to automate the deployment of Fabric items across different environments (DEV, TEST, PROD) using Azure DevOps pipelines and also rest API for creating the deployment pipeline


### Prerequisites
- Azure DevOps account with appropriate permissions
- Microsoft Fabric workspace(s) for deployment
- (optional) Service Principal configured with appropriate access to Fabric workspaces # we can also use user login
- Python 3.9+ installed on your development machine


## Deployment Options
- This repository demonstrates two yaml pipelines, onve for deploying the resources/iteam in fabric workspace 
- second pipeline is to create the deployment pipeline and attach the workspace to them


## git 
- git add .
- git commit -m "some message"
- git pull origin master --rebase
- git rebase --continue   # only if conflict apper again 
- git push origin master

## git errors:
- git pull origin master --no-rebase
- git push origin master

## get resource ids
- fab config set mode interactive
- fab auth login
- cd DEWorkshop_raziuddinkhazi_dev.Workspace


## pre-commit hooks 
- mkdir -p .git/hooks
- touch .git/hooks/pre-commit
- chmod +x .git/hooks/pre-commit


## diable and enable pre-commit hooks
- cd .git/hooks
- mv pre-commit pre-commit.disabled


- mv pre-commit.disabled pre-commit   # re-enable

# temporary skip
- git commit clear


## deployment pipeline
- az login
- az account get-access-token --resource https://api.fabric.microsoft.com

next tasks:
- ipynb kind of notebook (handy to code from local)
- run the data pipeline automatically (trigger not possible at the moment)
- deploy the variable group later 
- connect lakehouse to respective notebooks, currently done manually


# running the create_custom_envs.py
- python your_script.py --overwrite_whl yes --token eyJ0eXAiOiJKV1QiLCJhb...
