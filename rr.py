import aiohttp


class Gemini:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def ask(self, prompt: str, file: dict = {}) -> dict:
        async with aiohttp.ClientSession() as session:
            payload = {}
            payload["contents"] = []
            if file:
                file_uri = file["file"]["uri"]
                payload["contents"].append(
                    {
                        "role": "user",
                        "parts": [
                            {
                                "fileData": {
                                    "fileUri": file_uri,
                                    "mimeType": "image/jpeg"
                                }
                            },
                            {
                                "text": prompt
                            }
                        ]
                    }
                )
            else:
                payload["contents"].append(
                    {
                        "role": "user",
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                )
            payload["generationConfig"] = {
                "temperature": 0.9,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024,
                "responseMimeType": "text/plain"
            }
            async with session.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-8b-exp-0924:generateContent?key={self.api_key}", headers={"Content-Type": "application/json"}, json=payload) as response:
                try:
                    results = await response.json()
                    return results
                except Exception as e:
                    return {"error": str(e)}

    async def upload_image(self, path: str) -> dict:
        with open(path, "rb") as file:
           async with aiohttp.ClientSession() as session:
               payload = {"file": file}
               async with session.post(f"https://generativelanguage.googleapis.com/upload/v1beta/files?key={self.api_key}", data=payload) as response:
                   try:
                       return await response.json()
                   except Exception as e:
                       return {"error": str(e)}
        os.remove(path)
 
