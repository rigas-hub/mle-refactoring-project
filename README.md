# Refactoring Project

This repository is a **learning template for refactoring a data science project**. It starts with a notebook that analyzes King County house sales and guides you in moving its data-cleaning and feature-engineering steps into reusable Python code. The main project goal is to build a pipeline that prepares the data consistently; model training, predictions, and the FastAPI service show how that prepared data can be used in a wider application.

## Project Goal and Learning Objectives

The primary goal is to refactor the notebook's data preparation into a reusable pipeline. As you work through the project, you will learn to:

- Understand an existing data science notebook well enough to identify and extract its preprocessing steps.
- Organize data cleaning and feature engineering into reusable Python functions.
- Build and run a pipeline that prepares the house-price data.
- Train a model and use it to predict house prices.
- Store house data in a local database and expose it through a FastAPI service that can return predictions.

## Learning Path

| File / Folder | Description |
|---|---|
| [**Project Description**](project-description.md) | The assignment tasks and stretch goals. |
| [**King County Notebook**](King-County.ipynb) | The original notebook: EDA, cleaning, feature engineering, and modeling for King County house prices. |

### Additional Folders and Files

| File / Folder | Description |
|---|---|
| [**data/**](data/) | King County house price dataset used for data preparation and model training. |
| [**assets/**](assets/) | Visual aids referenced by the project. |
| [**src/**](src/) | Data preparation, feature engineering, model training, and standalone prediction scripts. |
| [**service/**](service/) | FastAPI endpoints, SQLite database setup, and house data models. The local `houses.db` database is created when the service starts. |
| [**model/**](model/) | Trained model saved as `model.bin`; used by the prediction scripts and FastAPI endpoint. |
| [**tests/**](tests/) | Tests for the data preparation pipeline and FastAPI service. |
| [**.python-version**](.python-version) | Python version range used by the project. |
| [**pyproject.toml**](pyproject.toml) | Project metadata, dependencies, and FastAPI entry point. |
| [**uv.lock**](uv.lock) | Locked dependency versions for reproducible setup. |

## Setup

Use [uv](https://docs.astral.sh/uv/getting-started/installation/) 0.13.5 or newer
and Python 3.13.17 or a newer 3.13 patch release, as defined in
[`.python-version`](.python-version).

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

## How to Use This Repo

1. Read the assignment brief in [project-description.md](project-description.md).
2. Work through the notebook in [King-County.ipynb](King-County.ipynb).
3. Use `data_preperation_pipeline(data_path)` in
   [src/data_pipeline.py](src/data_pipeline.py) to clean the data and create
   features. It reads the CSV and returns a prepared DataFrame.
4. Train and save the model from the project root:

   ```powershell
   uv run python src/model_training.py
   ```

   The training script reports an evaluation score and saves the trained model
   as `model/model.bin`. To run the standalone sample prediction script:

   ```powershell
   uv run python src/prediction_app.py
   ```

5. Start the FastAPI app from the project root:

   ```powershell
   uv run fastapi dev
   ```

   The service uses SQLite and creates `service/houses.db` automatically.
   Entries are kept between runs; no database server or `.env` configuration
   is needed. Open
   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to try the API.

6. In the interactive docs, create a house using `POST /houses`. For example:

   ```json
   {
     "id": 1,
     "bedrooms": 3,
     "grade": 7,
     "last_known_change": 2015,
     "center_distance": 2.5
   }
   ```

7. Request a price prediction for that saved entry using
   `GET /houses/{house_id}/prediction`. For the example above, request
   `GET /houses/1/prediction`. The endpoint reads `grade`,
   `last_known_change`, and `center_distance` from the saved house and sends
   those features to the model at `model/model.bin`.

The API also lets you list houses (`GET /houses`), retrieve one house
(`GET /houses/{house_id}`), replace its feature values
(`PUT /houses/{house_id}`), and delete it (`DELETE /houses/{house_id}`).

The service code is split into a few small parts:

- [service/main.py](service/main.py) defines the API endpoints, including
  prediction for a saved house.
- [service/schemas.py](service/schemas.py) defines the request and response data.
- [service/models.py](service/models.py) describes how houses are stored.
- [service/database.py](service/database.py) configures SQLite and provides a
  database session for each request.

## Project Reflection (as submitted on 29 October 2026)

### What steps did you take to complete the project?

I started by exploring the notebook, identifying data-quality issues, and
deciding how to clean the data and create useful features. I then moved the
preprocessing steps into reusable transformers and a scikit-learn pipeline,
trained a model using selected features, and added a script to make predictions
with the saved model.

I also built a simple FastAPI service backed by a local SQLite database. It
saves house data and uses a saved house's features to request a house-price
prediction from the trained model.

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
