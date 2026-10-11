✈️ SkyPulse — Airline Operations Intelligence

SQL Analytics Portfolio Project | MariaDB

SkyPulse is an airline operations analytics project built using MariaDB and SQL. It explores flight delays, cancellations, airline performance, airport routes, and operational efficiency using synthetic flight data.

📊 Project Overview

Database: MariaDB 11.8

Dataset: 1,000 synthetic flight records

Tables: airlines, airports, flights, delay_reasons

Analytics: Flight delay rates, cancellation rates, route performance, and delay reasons

🛠️ SQL Skills Demonstrated

Relational database design

Primary keys and foreign keys

INNER JOIN and multi-table JOIN

GROUP BY and ORDER BY

COUNT, SUM, AVG, and ROUND

CASE WHEN conditional aggregation

SQL views

Stored procedures for synthetic data generation

📈 Key Analyses

1. Airline Performance

Compare airlines by total flights, delayed flights, and delay percentages.

2. Flight Delay and Cancellation KPIs

Measure overall delay and cancellation rates.

3. Route Analytics

Identify the busiest flight routes and compare their average departure delays.

4. Delay Reason Analysis

Explore operational factors such as weather, technical issues, crew delays, and air traffic.

🗂️ Database Structure

Table

Purpose

airlines

Airline information

airports

Airport locations and codes

flights

Flight schedules, statuses, and delays

delay_reasons

Reasons for flight delays

The flights table connects airlines and airports through foreign keys. The delay_reasons table connects to individual flights.

🚀 How to Run

Install MariaDB.

Download skypulse_database.sql.

Import the database using:

mariadb -u root -p < skypulse_database.sql

Open MariaDB and run:

USE skypulse_db;
SELECT * FROM airline_performance;

Depending on your MariaDB authentication setup, the import command may need to be adjusted.

📁 Project Files

skypulse_database.sql — Database structure, synthetic data, and SQL view

README.md — Project documentation

⚠️ Data Disclaimer

All flight records are synthetic and intended for educational and portfolio demonstration purposes. The results do not represent actual airline performance.

🎯 Project Objective

Demonstrate practical SQL skills by transforming relational flight data into useful operational KPIs and business insights.# SkyPulse-Airline-Operations
SQL-based airline operations and flight delay analytics using MariaDB and synthetic data
