# Remarkable Morning News 📰

Автоматическая доставка новостей из RSS-потоков на ваш reMarkable в формате PDF.

## 📋 Описание

Проект автоматизирует процесс получения новостей из RSS-источников, формирования PDF-документа и загрузки в облако reMarkable. После синхронизации устройства свежие новости будут доступны для чтения на вашем reMarkable.

**Технологический стек:**
- 🐳 Docker & Docker Compose
- 🔄 n8n (workflow automation)
- 📄 Gotenberg (PDF generation)
- ☁️ rmapi (reMarkable Cloud API)

## 🚀 Быстрый старт

### Предварительные требования

- Docker и Docker Compose
- Аккаунт reMarkable
- Git

### Установка

1. **Клонируйте репозиторий:**

```bash
git clone https://github.com/ktibr0/Remarkable_morning_news
cd Remarkable_morning_news
```

2. **Создайте необходимые директории и установите права:**

```bash
mkdir -p ./config ./data ./app
sudo chown -R 1000:1000 ./data ./config ./app
```

3. **Запустите контейнеры:**

```bash
docker compose up -d --build
```

4. **Проверьте статус контейнеров:**

```bash
docker ps
```

## 🔑 Настройка аутентификации reMarkable

1. **Найдите и войдите в контейнер rmapi:**

```bash
docker ps | grep remarkable_morning_news-rmapi
```

> ⚠️ **Важно:** Используйте container-id запущенного `remarkable_morning_news-rmapi`, а **не** `remarkable_morning_news-rmapi_api`

```bash
docker exec -it <rmapi-container-id> /bin/sh
```

2. **Инициализируйте rmapi:**

```bash
rmapi
```

3. **Получите код подтверждения:**

При первом запуске rmapi запросит код подтверждения. Откройте в браузере:

```
https://my.remarkable.com/device/browser?showOtp=true
```

Скопируйте показанный код и вставьте его в терминал контейнера.

4. **Проверьте подключение:**

```bash
rmapi ls
```

Вы должны увидеть список файлов и папок из вашего reMarkable Cloud.

5. **Выйдите из контейнера:**

```bash
# Нажмите Ctrl+D или введите:
exit
```

## ⚙️ Настройка n8n

### Установка Community Node для Gotenberg

1. Откройте интерфейс n8n
2. Перейдите в **Settings → Community nodes → Install**
3. В поле **npm Package Name** введите:
   ```
   n8n-nodes-gotenberg-pdf
   ```
4. Нажмите **Install**

### Создание Credentials для Gotenberg

1. Перейдите в **Credentials → Add Credential**
2. Выберите **Gotenberg API**
3. Заполните поля:
   - **Base URL:** адрес развернутого сервиса Gotenberg
   - **Port:** `3000` (если не меняли при установке)
   
> ⚠️ **Важно:** Не ставьте обратный слэш после адреса. Правильный формат: `http://gotenberg:3000`

4. Сохраните. При сохранении произойдет попытка подключения к сервису.

### Импорт Workflow

**Вариант 1: Импорт по URL**

1. Создайте новый workflow
2. Выберите **Import from URL**
3. Укажите:
   ```
   https://raw.githubusercontent.com/ktibr0/Remarkable_morning_news/refs/heads/main/Remarkable_morninig_news.json
   ```

**Вариант 2: Импорт из файла**

1. Скачайте файл `Remarkable_morninig_news.json`
2. В n8n выберите **Import from File**
3. Загрузите скачанный файл

### Настройка нод Workflow

1. **Schedule Trigger:** Укажите периодичность запуска workflow
2. **RSS Read:** Укажите адрес RSS-потока
3. **Limit:** Установите лимит новостей (опционально)
4. **Gotenberg:** Выберите созданный ранее credential
5. **HTTP Request:** Укажите адрес развернутого сервиса `rmapi_api`

#### Настройка папки для новостей

В ноде **HTTP Request** есть параметр `folder` (по умолчанию: `News`).

**Опции:**
- ✅ **Рекомендуется:** Создайте папку `News` в облаке reMarkable через приложение или на устройстве
- 📁 Используйте свою папку: создайте папку с любым названием и укажите его в параметре `folder`
- 🗂️ Без папки: удалите параметр `folder`, новости будут в корневой директории

6. **Сохраните и активируйте workflow**

## 🎨 Кастомизация

Workflow построен модульно — вы можете добавлять любые шаги обработки новостей:
- Фильтрация по ключевым словам
- Перевод текста
- Суммаризация статей
- Дополнительное форматирование

Главное — сохранить "последнюю милю": формирование PDF через Gotenberg и загрузку в reMarkable через rmapi.

## 📚 Полезные ссылки

- [rmapi - reMarkable Cloud API](https://github.com/ddvk/rmapi)
- [Gotenberg - PDF generation service](https://github.com/gotenberg/gotenberg)
- [n8n Documentation](https://docs.n8n.io/)

## 🤝 Вклад в проект

Приветствуются pull requests и issues с предложениями по улучшению!

## 📄 Лицензия

MIT

---

**Создано с ❤️ для владельцев reMarkable**