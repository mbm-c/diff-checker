# Diff Checker

A simple and intuitive diff checker application built with Python and Streamlit. Compare two texts side-by-side and visualize the differences between them.

## Features

- 🎯 Two input fields for comparing texts
- 📊 Unified diff output format
- 🎨 Side-by-side HTML diff visualization with color coding
- 📈 Diff statistics (line counts, difference count)
- 💻 Clean and modern UI
- 🔒 **Privacy-first**: No logging, no data collection, completely secure

## Installation

This project uses `uv` for package management. Make sure you have `uv` installed.

1. Install dependencies:
```bash
uv sync
```

## Usage

Run the Streamlit application:

```bash
uv run streamlit run main.py
```

The application will open in your default web browser. You can:

1. Enter your first text in the "Text 1" field
2. Enter your second text in the "Text 2" field
3. Click the "Compare" button to see the differences

## Output Formats

The application provides two diff visualization options:

1. **Unified Diff**: Standard unified diff format showing additions and deletions
2. **Side-by-Side HTML Diff**: Visual HTML diff with color-coded changes (green for additions, red for deletions)

## Privacy & Security

**Your data is completely private and secure:**

- ✅ **No logging**: The application does not log, store, or track any content you enter
- ✅ **No data collection**: Your inputs are processed in memory only and never stored
- ✅ **No external requests**: Your data is never sent to third-party services
- ✅ **No persistence**: Your data is never saved to files or databases
- ✅ **In-memory processing**: All diff calculations happen in server memory and are discarded after processing

This application processes your text in memory on the server. Your data is only kept temporarily during 
the comparison and is immediately discarded. We have no way to see, access, or store your content 
after the session ends.

## Requirements

- Python >= 3.13
- Streamlit >= 1.28.0

## Deployment

### Streamlit Community Cloud (Recommended)

Streamlit Community Cloud is the easiest way to deploy this application for free. **Note:** GitHub Pages cannot host Streamlit apps as it only serves static files, while Streamlit requires a Python server.

#### Steps to Deploy:

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository and branch
   - Set the main file path to `main.py`
   - Click "Deploy"

3. **Your app will be live at:** `https://your-app-name.streamlit.app`

The `requirements.txt` file is already included for Streamlit Cloud to install dependencies.

### Alternative Deployment Options

If you prefer other platforms:

- **Render**: Add a `render.yaml` or use their web service
- **Railway**: Connect your GitHub repo and deploy
- **Heroku**: Use a `Procfile` with `web: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0`
- **Fly.io**: Use their platform with Docker or their Python buildpack

