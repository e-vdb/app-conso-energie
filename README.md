# Energy consumption web application

[![Python](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/downloads/release/python-3100/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://timothycrosley.github.io/isort/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://e-vdb-app-conso-energie-src01--accueil-8o2hdv.streamlit.app/)
![monthly_reminder](https://github.com/e-vdb/app-conso-energie/actions/workflows/run_app.yml/badge.svg)

## 🚀 Features

- Connect to a private google sheet
- Store meter readings (electricity, gas, water, ...)
- Visualize consumption
- Export/send yearly reports (🚧)
- Remind user by email to update the meter readings

## 📋 Tasks list

- [x] Store and load data from private google sheet
- [x] Create the streamlit app with following pages
  - [x] Home page
  - [x] Meter readings page
  - [x] Consumption page
- [x] Content of the meter readings page
  - [x] See the meter readings
  - [x] Add a new entry
  - [x] Edit an entry
- [x] Content of the consumption page
  - [x] Total consumption (table and charts)
  - [x] Annual consumption (table and charts)
  - [x] Compare consumption with previous years
- [x] Deploy the app on Streamlit Cloud
- [x] Add a reminder to update the meter readings (email) with a cron job
- [ ] Export/send yearly report
