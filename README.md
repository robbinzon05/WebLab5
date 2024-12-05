# WebLab5

## Awaited fixes (temporary section):
- Починить регистрацию, после регистрации перенаправляет на home, но мы не авторизованы, также нельзя войти. - Не создаются пользователи в базе данных.

## Technological Stack

- **SPA -** vue3 + typescript + design system
- **REST -** DRF
- **Docker**
- **CI -** github actions/buildbot/etc...
- **Websockets**

## Backend start

```bash
python -m venv venv # create virtual environment
pip install -r requirements.txt # install python dependencies
venv\Scripts\activate # activate virtual environment

cd backend
python manage.py migrate # migrate to the database
python manage.py runserver # start the server
```

## Frontend start

```bash
cd frontend
npm install # install dependencies
npm run serve # run local dev server
```
