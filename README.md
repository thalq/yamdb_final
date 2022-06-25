
![yamdb_final](https://github.com/thalq/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# Финальный проект «yamdb_final»

## Описание проекта
> *Этот API даёт возможность взаимодействовать с сайтом и пользоваться функционалом, не заходя на сайт. В нём доступны следующие действия:*
----

### :closed_lock_with_key: AUTH
###### _Регистрация пользователей и выдача токенов_

**Регистрация нового пользователя**
- Получить код подтверждения на переданный email.
- Права доступа: Доступно без токена.
- Использовать имя 'me' в качестве username запрещено.
- Поля email и username должны быть уникальными.

**Получение JWT-токена**
- Получение JWT-токена в обмен на username и confirmation code.
- Права доступа: Доступно без токена.
----

### :cinema: CATEGORIES
###### _Категории (типы) произведений_

**Получение списка всех категорий**
- Получить список всех категорий
- Права доступа: Доступно без токена

**Добавление новой категории**
- Создать категорию.
- Права доступа: Администратор.
- Поле slug каждой категории должно быть уникальным.

**Удаление категории**
- Удалить категорию.
- Права доступа: Администратор.
----

### :performing_arts: GENRES
###### _Категории жанров_

**Получение списка всех жанров**
- Получить список всех жанров.
- Права доступа: Доступно без токена

**Добавление жанра**
- Добавить жанр.
- Права доступа: Администратор.
- Поле slug каждого жанра должно быть уникальным.

**Удаление жанра**
- Удалить жанр.
- Права доступа: Администратор.
----

### :clapper: TITLES
###### _Произведения, к которым пишут отзывы (определённый фильм, книга или песенка)_

**Получение списка всех произведений**
- Получить список всех объектов.
- Права доступа: Доступно без токена

**Добавление произведения**
- Добавить новое произведение.
- Права доступа: Администратор.
- Нельзя добавлять произведения, которые еще не вышли (год выпуска не может быть больше текущего).
- При добавлении нового произведения требуется указать уже существующие категорию и жанр.

**Получение информации о произведении**
- Информация о произведении
- Права доступа: Доступно без токена

**Частичное обновление информации о произведении**
- Обновить информацию о произведении
- Права доступа: Администратор

**Удаление произведения**
- Удалить произведение.
- Права доступа: Администратор.
----

### :pencil: REVIEWS

###### _Отзывы_

**Получение списка всех отзывов**
- Получить список всех отзывов.
- Права доступа: Доступно без токена.

**Добавление нового отзыва**
- Добавить новый отзыв. Пользователь может оставить только один отзыв на произведение.
- Права доступа: Аутентифицированные пользователи.

**Полуение отзыва по id**
- Получить отзыв по id для указанного произведения.
- Права доступа: Доступно без токена.

**Частичное обновление отзыва по id**
- Частично обновить отзыв по id.
- Права доступа: Автор отзыва, модератор или администратор.

**Удаление отзыва по id**
- Удаление отзыва по id
- Права доступа: Автор отзыва, модератор или администратор.
----

### :+1::-1:COMMENTS

###### _Комментарии к отзывам_

**Получение списка всех комментариев к отзыву**
- Получить список всех комментариев к отзыву по id
- Права доступа: Доступно без токена.

**Добавление комментария к отзыву**
- Добавить новый комментарий для отзыва.
- Права доступа: Аутентифицированные пользователи.

**Получение комментария к отзыву**
- Получить комментарий для отзыва по id.
- Права доступа: Доступно без токена.

**Частичное обновление комментария к отзыву**
- Частично обновить комментарий к отзыву по id.
- Права доступа: Автор комментария, модератор или администратор.

**Удаление комментария к отзыву**
- Удалить комментарий к отзыву по id.
- Права доступа: Автор комментария, модератор или администратор.
----

### :bowtie: USERS

###### _Пользователи_

**Получение списка всех пользователей**
- Получить список всех пользователей.
- Права доступа: Администратор

**Добавление пользователя**
- Добавить нового пользователя.
- Права доступа: Администратор
- Поля email и username должны быть уникальными.

**Получение пользователя по username**
- Получить пользователя по username.
- Права доступа: Администратор

**Изменение данных пользователя по username**
- Изменить данные пользователя по username.
- Права доступа: Администратор.
- Поля email и username должны быть уникальными.

**Удаление пользователя по username**
- Удалить пользователя по username.
- Права доступа: Администратор.

**Получение данных своей учетной записи**
- Получить данные своей учетной записи
- Права доступа: Любой авторизованный пользователь

**Изменение данных своей учетной записи**
- Изменить данные своей учетной записи
- Права доступа: Любой авторизованный пользователь
- Поля email и username должны быть уникальными.
----

## :wrench: Установка
:white_check_mark: Клонируем репозиторий:

```$ git clone git@github.com:thalq/yamdb_final.git```

:white_check_mark:  Создаем виртуальное окружение:
 
 ```$ python -m venv venv```
 
 :white_check_mark: Устанавливаем зависимости:

```$ pip install -r api_yamdb/requirements.txt```

 :white_check_mark: Переходим в папку Docker-compose.yaml:

```$ cd infra```

 :white_check_mark: Поднимаем контейнеры:

```$ docker-compose up -d --build```

:white_check_mark: Выполняем миграции:

```$ docker-compose exec web python manage.py makemigrations reviews``` затем ```$ docker-compose exec web python manage.py migrate --run-syncdb```

:white_check_mark: Создаем суперпользователя:

```$ docker-compose exec web python manage.py createsuperuser```

:white_check_mark: Собираем статику:

```$ docker-compose exec web python manage.py collectstatic --no-input```

:white_check_mark: Останавливаем контейнеры:

```$ docker-compose down -v```

----

## :bulb: Примеры
**_1. Перейти на страницу администратора_**

```
http://84.201.162.216/admin/
```

**_2. Перейти на страницу redoc_**

```
http://84.201.162.216/redoc/
```

### Для формирования запросов и ответов использована программа [Postman](https://www.postman.com/).

**_3. Получение списка всех произведений_**

###### _Передаем GET-запрос к эедпоинту TITLES:_
```
http://84.201.162.216/api/v1/titles/
```

<p align="center">:arrow_down:<p align="center">
 
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
          {
            "name": "string",
            "slug": "string"
          }
        ],
        "category": {
          "name": "string",
          "slug": "string"
        }
      }
    ]
  }
]
```
 
 
**_4. Регистрация нового пользователя_**
 
######  _Передаем POST-запрос на эндпоинт AUTH_
```
 http://84.201.162.216/api/v1/auth/signup/
 ```
 
 ######  _с параметрами:_
 
 ```
 {
  "email": "string",
  "username": "string"
}
 ```
 
 <p align="center">:arrow_down:<p align="center">
  
 ```
{
  "email": "string",
  "username": "string"
}
```
  
  
**_5. Полуение отзыва по id_**
  
###### _Передаем GET-запрос к эедпоинту REVIEWS_
  
```
http://84.201.162.216/api/v1/titles/{title_id}/reviews/{review_id}/
```
  
<p align="center">:arrow_down:<p align="center">

```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```
 