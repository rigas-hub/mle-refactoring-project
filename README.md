# Refactoring Project

Use this repository as a **template** for your refactoring project. It walks you through turning a working but messy notebook into clean, reusable Python code: the notebook analyzes King County house sales, and your job is to extract its data cleaning and feature engineering logic into a proper pipeline. Create pull requests in your own copy even if you are working alone, and use them to track your progress.

## Learning Objectives

By the end of this repository, you should be able to:

- Read and understand an existing Data Science notebook well enough to refactor it.
- Refactor data cleaning and feature engineering code into reusable Python functions.
- Build a pipeline that reproduces a notebook's preprocessing steps end to end.
- Apply the same refactoring approach to a modeling workflow (stretch goal).
- Build and containerize a FastAPI CRUD service backed by a database (stretch goal).

## Learning Path

| File / Folder | Description |
|---|---|
| [**Project Description**](project-description.md) | The assignment tasks and stretch goals. |
| [**King County Notebook**](King-County.ipynb) | The original notebook: EDA, cleaning, feature engineering, and modeling for King County house prices. |

### Additional Folders and Files

| File / Folder | Description |
|---|---|
| [**data**](data/) | The King County house price dataset used by the notebook. |
| [**assets**](assets/) | Visual aids referenced in the repository. |
| [**bonus_solution**](bonus_solution/) | A FastAPI + Postgres + Docker reference implementation for the optional CRUD stretch goal. |
| [**pyproject.toml**](pyproject.toml) | Project configuration and dependencies. |
| [**uv.lock**](uv.lock) | Dependency lock file. |

## Setup

Use [uv](https://docs.astral.sh/uv/getting-started/installation/) 0.13.5 or newer
and Python 3.13.17 or a newer 3.13 patch release, as defined in
[`.python-version`](.python-version).

Rebuild existing Docker images with `--pull --no-cache` after this update
to refresh their system certificates and dependencies.

> [!NOTE]
> Throughout these steps, text in angle brackets like `<repo-name>` is a **placeholder**. Replace it, including the `< >` brackets, with your own value. For example, `cd <repo-name>` becomes `cd mle-refactoring-project`.

### 1. Create the Repository from the Template

Click **Use this template** on GitHub.

When creating the repository:

- Set yourself as the **Owner**
- Choose a repository name
- Disable **Include all branches**
- Click **Create repository**

> [!IMPORTANT]
> If you are working in pairs or groups, only **one person** should complete this step.

---

### 2. Add Collaborators (Pairs/Groups Only)

If working with teammates:

1. Open the repository on GitHub
2. Go to **Settings → Collaborators**
3. Add your teammates as collaborators
4. Share the repository link with your team

Teammates should accept the invitation before continuing.

---

### 3. Clone the Repository

Copy the SSH URL from the **Code** button on GitHub, then run:

```bash
git clone <copied-ssh-url>
```

The copied SSH URL will look like `git@github.com:<your-username>/<repo-name>.git`.

---

### 4. Move into the Project Folder and Install Dependencies

This installs all dependencies and creates a virtual environment in `.venv/`.

```bash
cd <repo-name>
uv sync
```

---

### 5. Open the Repository in VS Code

> [!NOTE]
> Make sure you open VS Code from the project root so it automatically detects the environment created by `uv sync`.

Launch VS Code in the project root folder:

```bash
code .
```

Then open [King-County.ipynb](King-County.ipynb) and select the Python environment created by `uv sync` as the kernel.

---

### 6. Clean the data and create features

The `data_preperation_pipeline(data_path)` function in
[src/data_pipeline.py](src/data_pipeline.py) reads the CSV file, applies the
data-cleaning and feature-engineering transformers, and returns the resulting
DataFrame. It can be called from other Python code and is used by the
model-training workflow.

### 7. Train the model

Run the model-training script from the project root. It calls the data
preparation function, trains a linear regression model, prints its test score
and a sample prediction, and saves the trained model.

```bash
uv run python src/model_training.py
```

### 8. Make a prediction

After training, run the prediction script to load the saved model and predict
a house price from the sample features defined in the script:

```bash
uv run python src/prediction_app.py
```

## How to Use This Repo

1. Read the assignment brief in [project-description.md](project-description.md).
2. Work through the notebook in [King-County.ipynb](King-County.ipynb).
3. Refactor the cleaning and feature engineering logic into Python files.
4. Build a reusable pipeline.
5. If you want an extra challenge, extend your refactor to cover the modeling step as well.
6. If you want to go even further, use [bonus_solution/](bonus_solution/) as a reference for the optional FastAPI + Docker stretch goal.

## Bonus Solution

The [bonus_solution/](bonus_solution/) folder contains a minimal working example of:

- a FastAPI CRUD API
- Postgres persistence
- a `Dockerfile` for the API
- a `docker-compose.yaml` file to run the API and database together

It is included as a reference implementation for the optional stretch task, not as a required project structure.

## Project Reflection

### What steps did you take to complete the project?

I started by exploring the notebook, identifying data-quality issues, and
deciding how to clean the data and create useful features. I then moved the
preprocessing steps into reusable transformers and a scikit-learn pipeline,
trained a model using selected features, and added a script to make predictions
with the saved model.

As an additional challenge, I began building a simple FastAPI service backed by
a database containing house data. The longer-term goal is to use data submitted
to the service to generate house-price predictions.

### What challenges did you face?

Moving exploratory notebook code into Python modules required me to think about
software structure, dependencies, and how to make the workflow straightforward
to run. Learning to build and use data-processing pipelines was new to me and
became one of the most valuable parts of the project.

The API and database work was also challenging because I had limited experience
with those technologies. It gave me an opportunity to learn how a service might
receive and store house data.

### What would you do differently with more time?

I would improve the project’s usability, expand the tests, and explore the
modeling process further. The current modeling work focuses mainly on refactoring
the notebook’s workflow rather than comparing and tuning a broader range of
models. The existing test coverage is limited, so I would add tests to verify
the behavior of the preprocessing pipeline, model training, and prediction
workflow. I would also like to add more documentation to the code. It may not
be the most exciting part of engineering, but it would make the project easier
for others (and future me) to understand and maintain.

This project is still a work in progress, and I plan to continue improving it.
I learned a lot while working on it and would welcome constructive feedback.
