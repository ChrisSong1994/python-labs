from dotenv import load_dotenv
import os


def load_env():
    load_dotenv()
    print("Environment variables loaded.")
    return os.environ
