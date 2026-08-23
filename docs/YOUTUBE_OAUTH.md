# YouTube OAuth — AI Kamai Lab

## One-time authorization

1. In Google Cloud Console, use the project containing the YouTube Data API v3 and YouTube Analytics API.
2. Configure Google Auth Platform branding and audience. Add the Google account that owns **AI Kamai Lab** as a test user if the app is in testing.
3. Create a Desktop OAuth client named `AI Kamai Lab Automation`.
4. Download the OAuth client JSON locally. Do not commit it to GitHub.
5. Run the local OAuth bootstrap in the application when implemented. The browser will open Google's consent screen.
6. Sign in with the Google account that owns `AI Kamai Lab` and approve the requested YouTube scopes.
7. Store the resulting refresh token only in the deployment secret store.

## Required scopes

- `https://www.googleapis.com/auth/youtube.upload`
- `https://www.googleapis.com/auth/youtube.readonly`
- `https://www.googleapis.com/auth/yt-analytics.readonly`

## Security

Never paste client secrets, access tokens, or refresh tokens into chat, source files, issues, or commits. The application should load OAuth credentials from environment variables or a managed secret store.
