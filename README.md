# Visualisation - Python
> Instructions for getting started with Visualisations Python group

## About The Project

Live version: https://ifoa-dataviz-python.herokuapp.com/

The code in this repo is that developed by Afzaal Ahmed for the IFoA Data Science Working Party - Visualisation Worksteam. The private repo for the WP visualisation group can be found here: https://github.com/IFoADataScienceResearch/Visualisation

This project uses the Plotly Dash library. The objective is to create a dashboard using the dataset: https://www.kaggle.com/floser/french-motor-claims-datasets-fremtpl2freq

## Getting Started

The code will be hosted on your local machine, and in order to run the code you will need the following installed locally:

- Python v3+
- pip package manager
- Git

The following Python packages are needed

- Dash
- Pandas
- Dash Bootstrap
- Numerize
- natsort

See here for instructions on the commands needed to install the above packages:

- https://dash.plotly.com/installation
- https://dash-bootstrap-components.opensource.faculty.ai/

Before cloning the repo locally, first run the following commands to ensure your system has Python, pip and Git installed:

```
python --version
pip --version
git --version
```

If the above are installed, you'll be presented with a version number after each command.

If you don't have any of the above installed then you'll get an error message or "command not found" message.

Guides on installing the above can be found here if needed:

- Python: https://docs.python.org/3/using/windows.html
- pip: https://pip.pypa.io/en/stable/installation/
- Git: https://github.com/git-guides/install-git

Any terminal capable of running pip and Git commands is suitable for use.

Any IDE is suitable for use. If you have an IDE with an integrated terminal it will make it a little easier to develop. [VS Code](https://code.visualstudio.com/) is open source and comes with a range of packages which integrate nicely with Python for debugging and Git, it also comes with a built-in terminal.

## Launching Project Code

Clone remote repo locally using command:

```
git clone https://github.com/afzaalpersonal/ActuarialPythonDashboard.git
```

This will open a popup for GitHub which prompts for login credentials to access the private repo.

Open the terminal and cd in the Python sub-directory of the local cloned repo.

Run the following command to launch local server:

```
python app.py
```

Open the following url in your browser to access the project:

- http://127.0.0.1:8050/

## Heroku deployment

Run the following commands to deploy to Heroku (https://ifoa-dataviz-python.herokuapp.com/)

```
git add .
git commit -am "Heroku update"
git push heroku master
```

## External Documentation

- Official Plotly Dash website: https://dash.plotly.com
- 3rd party introductory tutorial: https://realpython.com/python-dash/

## Troubleshooting

- pip install not working: https://stackoverflow.com/questions/39832219/pip-not-working-in-python-installation-in-windows-10

## License Declarations

Licenses for 3rd party bundled assets used in this project are listed below. This project will only use 3rd party assets licensed under MIT or GPL.

- No bundled resources at present.
