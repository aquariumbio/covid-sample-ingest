# Covid Sample Ingest
Python scripts for ingesting samples for the Covid19 surveillance testing workflow

## Requirements

* [Trident](https://github.com/klavinslab/trident)
* An Aquarium login

This library is designed to be run in a Visual Studio Code [dev container](https://code.visualstudio.com/remote-tutorials/containers/how-it-works). To take advantage of this environment, you will also need to:

* Install [Docker](https://www.docker.com/get-started)
* Install [Visual Studio Code](https://code.visualstudio.com/)

Running in this environment eliminates the need to install Trident or manage your Python version. 

## Setup
### 1. Clone
[git](https://git-scm.com/) with the command

```bash
git clone git@github.com:aquariumbio/covid-sample-ingest.git
```

### 2. Open in VS Code dev container
From a new VS Code window, open the `covid-sample-ingest` folder. You should see a dialog at the bottom right corner of the window that says **Folder contains a dev container configuration file. Reopen folder to develop in a container (learn more).** Select **Reopen in Container**. You can also click the green rectangle at the lower left corner and select **Remote-Containers: Reopen Folder in Container** from the menu that appears at the top of the window. 

### 3. Add credentials
In order to add credentials for your Aquarium instance(s), `cp util/secrets_template.json util/secrets.json`, and add your login and url information to the new file. You can have more than two instances, and the keys (e.g., `laptop` and `production`) can be changed to whatever you want them to be.

```json
{
  "laptop": {
    "login": "neptune",
    "password": "aquarium",
    "aquarium_url": "http://localhost/"
  },
  "production": {
    "login": "your_production_username",
    "password": "your_production_password",
    "aquarium_url": "production_production_url"
  }
}
```

## Usage
In progress...
