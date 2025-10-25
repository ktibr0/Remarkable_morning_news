# Remarkable Morning News 📰

Automatic delivery of news from RSS feeds to your reMarkable in PDF format.

## 📋 Description

This project automates the process of fetching news from RSS sources, generating PDF documents, and uploading them to reMarkable Cloud. After device synchronization, fresh news will be available for reading on your reMarkable.

**Technology Stack:**
- 🐳 Docker & Docker Compose
- 🔄 n8n (workflow automation)
- 📄 Gotenberg (PDF generation)
- ☁️ rmapi (reMarkable Cloud API)

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- reMarkable account
- Git

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/ktibr0/Remarkable_morning_news
cd Remarkable_morning_news
```

2. **Create necessary directories and set permissions:**

```bash
mkdir -p ./config ./data ./app
sudo chown -R 1000:1000 ./data ./config ./app
```

3. **Start the containers:**

```bash
docker compose up -d --build
```

4. **Check container status:**

```bash
docker ps
```

## 🔑 reMarkable Authentication Setup

1. **Find and access the rmapi container:**

```bash
docker ps | grep remarkable_morning_news-rmapi
```

> ⚠️ **Important:** Use the container-id of the running `remarkable_morning_news-rmapi`, **not** `remarkable_morning_news-rmapi_api`

```bash
docker exec -it <rmapi-container-id> /bin/sh
```

2. **Initialize rmapi:**

```bash
rmapi
```

3. **Get the confirmation code:**

On first launch, rmapi will request a confirmation code. Open in your browser:

```
https://my.remarkable.com/device/browser?showOtp=true
```

Copy the displayed code and paste it into the container terminal.

4. **Verify the connection:**

```bash
rmapi ls
```

You should see a list of files and folders from your reMarkable Cloud.

5. **Exit the container:**

```bash
# Press Ctrl+D or type:
exit
```

## ⚙️ n8n Configuration

### Install Community Node for Gotenberg

1. Open n8n interface
2. Navigate to **Settings → Community nodes → Install**
3. In the **npm Package Name** field, enter:
   ```
   n8n-nodes-gotenberg-pdf
   ```
4. Click **Install**

### Create Credentials for Gotenberg

1. Go to **Credentials → Add Credential**
2. Select **Gotenberg API**
3. Fill in the fields:
   - **Base URL:** address of the deployed Gotenberg service
   - **Port:** `3000` (if not changed during installation)
   
> ⚠️ **Important:** Do not add a trailing slash after the address. Correct format: `http://gotenberg:3000`

4. Save. Upon saving, a connection attempt to the service will be made.

### Import Workflow

**Option 1: Import from URL**

1. Create a new workflow
2. Select **Import from URL**
3. Specify:
   ```
   https://raw.githubusercontent.com/ktibr0/Remarkable_morning_news/refs/heads/main/Remarkable_morninig_news.json
   ```

**Option 2: Import from File**

1. Download the `Remarkable_morninig_news.json` file
2. In n8n, select **Import from File**
3. Upload the downloaded file

### Configure Workflow Nodes

1. **Schedule Trigger:** Set the workflow execution frequency
2. **RSS Read:** Specify the RSS feed URL
3. **Limit:** Set the news limit (optional)
4. **Gotenberg:** Select the previously created credential
5. **HTTP Request:** Specify the address of the deployed `rmapi_api` service

#### News Folder Configuration

The **HTTP Request** node has a `folder` parameter (default: `News`).

**Options:**
- ✅ **Recommended:** Create a `News` folder in reMarkable Cloud via the app or directly on the device
- 📁 Use your own folder: create a folder with any name and specify it in the `folder` parameter
- 🗂️ No folder: remove the `folder` parameter, news will go to the root directory

6. **Save and activate the workflow**

## 🎨 Customization

The workflow is built modularly — you can add any news processing steps:
- Keyword filtering
- Text translation
- Article summarization
- Additional formatting

The key is to preserve the "last mile": PDF generation via Gotenberg and upload to reMarkable via rmapi.

## 📚 Useful Links

- [rmapi - reMarkable Cloud API](https://github.com/ddvk/rmapi)
- [Gotenberg - PDF generation service](https://github.com/gotenberg/gotenberg)
- [n8n Documentation](https://docs.n8n.io/)

## 🤝 Contributing

Pull requests and issues with improvement suggestions are welcome!

## 📄 License

MIT

---

**Made with ❤️ for reMarkable owners**