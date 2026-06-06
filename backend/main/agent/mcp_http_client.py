import requests

class MCPHttpClient:
    def __init__(self, base_url: str="http://localhost:9000"):
        self.base_url = base_url

    def call_tool(self, name: str, arguments: dict):
        response = requests.post(
            f"{self.base_url}/callTool",
            json={"name": name, "arguments": arguments}
        )
        response.raise_for_status()

        return response.json()
