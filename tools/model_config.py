import os

DeepSeek_model_config = {
    "model": "deepseek-v4-pro",
    "base_url": "https://api.deepseek.com",
    "streaming": True,
    "api_key": os.environ.get("DEEPSEEK_API_KEY"),
}
