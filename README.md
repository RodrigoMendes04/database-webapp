# 🗄️ Databases Project — Planet Zoo Edition 🐾

This repository contains the project developed for the **Databases (CC2005)** course at the **FCUP**.  
The project was carried out during the **first semester of the second year** of the **Bachelor's in Computer Science**.

---

## 👥 Group Members

| Nº Mecanográfico | Name              |
|------------------|-------------------|
| 202009330        | João Levandeira   |
| 202308366        | Rodrigo Mendes    |

---

## 📚 Project Overview

The goal of this project was to design and implement a relational **database** inspired by the game **Planet Zoo**, and to develop a **Python-based WebApp** for interacting with the data.

The project includes:
- Database design and modeling  
- SQL scripts to create and populate the database with Planet Zoo-related data  
- Python WebApp using Flask for visualization and querying  

---

## 🗄️ Database Population

### ➡️ Data Sources:
- We used the dataset available [here](https://docs.google.com/spreadsheets/d/16ZLLyfAVrQwxqENqkYrrEvvicrX536iy-kZOWuEUjOA/edit?usp=sharing).

### ➡️ Population Method:
- The `Animais` table was populated via CSV conversion from Excel.  
- All other tables (`Continente`, `Dieta`, `Habitat`, `Origens`) were populated manually.

### ➡️ Number of entries per table:
| Table      | Number of Entries |
|------------|-------------------|
| Animais    | 130               |
| Continente | 7                 |
| Dieta      | 3                 |
| Habitat    | 7                 |
| Origens    | 327               |

---

## 🌐 Python Web Application

The WebApp was developed using **Flask** and provides several endpoints to interact with the database:

| Endpoint                    | Functionality                                                      |
|-----------------------------|--------------------------------------------------------------------|
| `/`                         | Home page                                                          |
| `/animais/`                | List all animals                                                   |
| `/animais/<int:id>/`       | Show details of a specific animal                                  |
| `/continentes/`            | List all continents                                                |
| `/continentes/<int:id>/`   | Show details of a continent and its associated habitats            |
| `/habitats/`              | List all habitats                                                  |
| `/habitats/<int:id>/`     | Show details of a habitat and associated animals                   |
| `/dietas/`                | List all diets                                                     |
| `/dietas/<int:id>/`       | Show details of a diet and animals with that diet                  |
| `/animal/search/<expr>/`  | Search animals by name                                              |

---

## 📊 Example SQL Query Explanation

The home page also displays summary statistics by running a SQL query to count entries in each table:
```sql
SELECT * FROM (
  SELECT COUNT(animal_id) AS num_animais FROM Animais
) a
JOIN (
  SELECT COUNT(continente_id) AS num_continentes FROM Continente
) b
JOIN (
  SELECT COUNT(dieta_id) AS num_dietas FROM Dieta
) c
JOIN (
  SELECT COUNT(habitat_id) AS num_habitats FROM Habitat
) d
JOIN (
  SELECT COUNT(animal) AS num_origens FROM Origens
) e;
```
**Explanation:**

- Each subquery counts the number of records in a specific table.
- These results are joined together to present a single row with the counts of all tables.
- The final result shows the total number of animals, continents, diets, habitats, and origin relationships in the database.

---

## 🛠️ Technologies Used

- **PostgreSQL / MySQL** — Relational Database
- **SQL** — Database creation and data manipulation
- **Python** — Back-end and WebApp logic
- **Flask** — Python web framework
- **Jinja2** — Templating engine
- **HTML / CSS / Bootstrap** — Front-end styling
- **SQLite (optional)** — For lightweight testing
