import os
from fastapi import FastAPI, Request
from typing import Dict

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, vulnerable world!"}

# ------------------------------------
# 1) Command Injection Vulnerability
# ------------------------------------
@app.post("/command-injection")
async def command_injection(request: Request):
    """
    Example of insecure command injection:
    Reads 'cmd' from JSON body and directly concatenates
    it into a shell command without any sanitization.
    """
    data = await request.json()
    cmd = data.get("cmd", "")

    # Deliberately unsafe: passing user-controlled input to os.system
    exit_code = os.system(f"echo {cmd}")
    return {"executed_command": f"echo {cmd}", "exit_code": exit_code}

# ------------------------------------
# 2) Eval Injection Vulnerability
# ------------------------------------
@app.post("/eval-injection")
async def eval_injection(body: Dict[str, str]):
    """
    Example of insecure eval injection:
    Reads 'expression' from JSON body and directly passes
    it to Python's eval() without any validation.
    """
    expression = body.get("expression", "")

    # Deliberately unsafe: using eval() on user input
    try:
        result = eval(expression)
    except Exception as e:
        return {"error": str(e)}
    return {"result": result}