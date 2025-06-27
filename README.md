# 🚀 Python HTTP Web Server Framework

A minimal Python Flask like Multithreaded HTTP web server framework built on top of `socketserver`.
It provides routing with path and path parameters, a file watcher for auto-reloading, response classes, and an HTTP request parser. 🐍🧠

## ✨ Features

- 🔀 **Routing**: Register routes with static or dynamic path parameters (e.g., `/user/<str:user_id>`)
- 🔄 **Auto-reload Watcher**: Automatically restarts the server when code changes are detected
- 📦 **Response Classes**: Easily return JSON or custom responses
- 🧾 **HTTP Request Parser**: Parses HTTP requests, headers, body, and query parameters
- 🧱 **Modular Structure**: Organize your app with modules and handlers

## ⚙️ Getting Started

### 📥 1. Install Requirements

No external dependencies required (uses Python standard library) ✅

### 🗂️ 2. Project Structure

```bash
.
├── app.py
├── framework/
│   ├── constants.py
│   ├── http/
│   │   ├── request.py
│   │   ├── responses.py
│   │   ├── server.py
│   │   └── status.py
│   ├── route/
│   │   ├── __init__.py
│   │   └── register.py
│   ├── utils.py
│   ├── watcher.py
│   └── web_app.py
└── user/
    ├── handler.py
    └── routes.py
```

### ▶️ 3. Running the Server

```sh
python app.py
```

✅ By default, the server runs with auto-reload enabled 🔁
🛑 To run without auto-reload:

```sh
python app.py --noreload
```

### 🛣️ 4. Defining Routes

Register routes in your module's `routes.py` using `register_routes`:

```python
from framework.route import register_routes
from .handler import create_user

register_routes(route="/user", handler_func=create_user, http_methods=["POST"])
register_routes(route="/user/<str:user_id>", handler_func=get_user, http_methods=["GET"])
```

📌 Supports path parameters:

- `<str:name>` for string 🔤
- `<int:id>` for integer 🔢

### 🧑‍🍳 5. Writing Handlers

Handlers receive a `Request` object and any path parameters:

```python
from framework.http.responses import JsonResponse

def get_user(request, user_id):
    # Your logic here
    return JsonResponse(data={"user_id": user_id})
```

### 📬 6. Response Classes

- `JsonResponse(data, status_code=200)`: Returns a JSON response 📄
- `BaseResponse`: Base class for custom responses 🧱

### 🕵️‍♂️ 7. HTTP Request Parsing

The framework parses:

- 🔡 HTTP method, path, version
- 🧾 Headers
- 🔍 Query parameters
- 🧪 JSON body (for `Content-Type: application/json`)

### 🛠️ 8. Auto-reload Watcher

The watcher monitors `.py` files and restarts the server on changes 🔁
Implemented in [`framework/watcher.py`](framework/watcher.py)

---

## 💡 Example

```python
# app.py
from framework.web_app import WebApp

app = WebApp()
app.modules(["user"])

if __name__ == "__main__":
    app.run(reload=True)
```

---

## 👨‍💻 Author

- 🧑‍💻 Bhushan Borse*
