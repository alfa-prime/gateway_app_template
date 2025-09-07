### Шаблон приложения для использования шлюза ЕВМИАС API.

1. Клонируем репозиторий с указанием папки (project_name)
```commandline
git clone ssh://git@gitverse.ru:2222/imperium/gateway_app_template.git project_name
```
**если имя проекта не указать, то установится по умолчанию в gateway_app_template**

2. Копируем `env.example` в `.env`
```commandline
cp .evn.example .env
```

и правим `.env` файл, подставляя свой апи ключ вместо `super-puper-secret-gateway-key`.
```
GATEWAY_API_KEY=super-puper-secret-gateway-key
```
3. `docker-compose.yml`  заменям `continer_name` на свое, например `my_super_app`
4. `docker-compose.prod.yml`  заменям `continer_name` на свое, например `my_super_app_prod`
5. `makefile` в разделе `Development` заменяем `gateway_template_app` на то что указали в `docker-compose.yml` в нашем случае `my_super_app`
6.  `makefile` в разделе `Production` заменяем `gateway_template_app_prod` на то что указали в `docker-compose.prod.yml` в нашем случае `my_super_app_prod`


**Запуск (разработка)**
```commandline
make up
```

**Запуск (прод)**
```
make up-prod
```

остальные команды смотри `makefile`