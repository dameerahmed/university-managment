from fastmcp import FastMCP
from uni.main import app


app = FastMCP.from_fastapi(app=app,name="students_management",version="1.0.0")

if __name__ == "__main__":
    app.run()
