# WebLab5

---

## Awaited Fixes and Work (temporary section):
- Сделать лобби и управление аккаунтом (выше, возможно в header) на одной страничке (Home) **и красиво**.
- Сделать у пользователя поле avatar_id (int) которое будет отвечать за выбранный аватар и сделать аватары, их выбор, платные аватары + их покупка и _все для профиля_ (в Home) до конца. _Все для профиля_ должно включать в себя смену имени и так далее.
- Настроить лобби так, чтобы при количестве игроков более 1 и при том что вы не глава лобби, при нажатии на соло игру вылезало предупреждение, что вы выйдете из лобби в новое пустое, а если вы создатель (и тоже игроков в вашем лобби больше 1), что лобби будет расформировано и вас так же выкенет из лобби в новое пустое. (Если игра мультиплеерная то перекидывает со всеми игроками в игру после решения главы лобби, а если соло то сразу запускается соло игра но вы в пустом своем лобби были.).
- _Починить наши игры_ - заглушки (проблема коммуникации с сервером есть сейчас).

### Design Ideas:
![image](https://github.com/user-attachments/assets/f544ee77-85b5-4502-9140-a5c0a65e9196)
- Только необходимо где то еще _профиль и управление профилем_ поместить. (**Как хотели - в header, раскрытие которого перекрывает другие элементы**).
- Лобби и ссылка (код) на лобби слева, участники слева в том же лобби, а игры справа + еще что останется куда-нибудь поместить. Сверху профиль и управление профилем (количество монет, получить монеты, сменить аватар и так далее).
- Можно менять чтобы нам подошло, но основная суть есть, (особенно с расположением игр - _игры все в одной секции и подпишем какая из них для одного игрока а какая - мультиплеерная_).

---

## Technological Stack

- **SPA -** vue3 + typescript + design system
- **REST -** DRF
- **Docker**
- **CI -** github actions/buildbot/etc...
- **Websockets**

## Backend start

```bash
python -m venv venv # create virtual environment
venv\Scripts\activate # activate virtual environment
pip install -r requirements.txt # install python dependencies

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
