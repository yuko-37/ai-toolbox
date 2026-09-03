### Vk video scrapper
This application monitors predefined VK video playlists that contain episodic shows and automatically retrieves the most recently published entries. It simply displays the latest available shows from each playlist, allowing users to quickly check whether new content has appeared and view the most recent episodes without manually browsing the playlists.

```bash
  docker build -t vkvideo-scrapper .
  docker run -p 8501:8501 vkvideo-scrapper
```
