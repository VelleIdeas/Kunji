# Kunji
This is the v1 code for Kunji project by Velle Ideas LLC.
This readme contains information to replicate the repo, build and run the apps/services.

# Instructions
Never check-in to master. Every contributer needs to create a Pull Request to commit any changes to master.

Git Setup:

1. Git HubFlow Installation
2. HubFlow Usage

# Git HubFlow Installation
HubFlow is:

an extension to the Git command-line tools
a fork of the original GitFlow tools
one-line commands for using the GitFlow branching model with GitHub
focused on making it as easy as possible to use GitFlow with GitHub
The main differences between the original GitFlow tools and HubFlow are:

by default, commands push to / pull from GitHub wherever it is appropriate
we’ve added additional commands (such as feature push and feature pull) to fill in some gaps in the original GitFlow tools

#### Installing HubFlow
Installing the HubFlow tools for the first time is very easy:
```
git clone https://github.com/datasift/gitflow
cd gitflow
sudo ./install.sh
```

#### Upgrading HubFlow
If you want to upgrade to the latest version of HubFlow, simply run:
```
sudo git hf upgrade
```

#### Listing The Available Commands
To see all of the commands that HubFlow provides, simply run:
```
git hf help
```

# HubFlow Usage

#### 1. Cloning A Repo
Clone the existing repo from GitHub to your local workstation:
git clone git@github.com:##orgname##/##reponame##
Please remember:
Do not fork the repo on GitHub - clone the master repo directly.

#### 2. Initialise The HubFlow Tools
The HubFlow tools need to be initialised before they can be used:
cd ##reponame##
git hf init
Please remember:
You have to do this every time you clone a repo.

#### 3. Create A Feature Branch
If you are creating a new feature branch, do this:
git hf feature start ##feature-name##
If you are starting to work on an existing feature branch, do this:
git hf feature checkout ##feature-name##

Please remember:
All new work (new features, non-emergency bug fixes) must be done in a new feature branch. Give your feature branches sensible names. If you’re working on a ticket, use the ticket number as the feature branch name (e.g. ticket-1234). If the feature branch already exists on the master repo, this command will fail with an error.

#### 4. Publish The Feature Branch On GitHub
Push your feature branch back to GitHub as you make progress on your changes:
git hf push

#### 5. Keep Up To Date
You’ll need to bring down completed features & hotfixes from other developers, and merge them into your feature branch regularly. (Once a day, first thing in the morning, is a good rule of thumb). if you're not on your feature branch
git hf feature checkout ##feature-name##

pull down master and develop branches

git hf update

merge develop into your feature branch

git merge develop

#### 6. Collaborate With Others
Push your feature branch back to GitHub whenever you need to share your changes with colleagues:

git hf push

Pull your colleague’s changes back to your local clone:

git hf pull

#### 7. Merge Your Feature Into Develop Branch

git hf push
