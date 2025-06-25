from framework.app import WebApp

app = WebApp()


app.modules(["user"])

if __name__ == "__main__":
    app.run()
