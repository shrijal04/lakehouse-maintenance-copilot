from pprint import pprint
import os

from dotenv import load_dotenv
from groq import Groq

from app.services.ai_report_service import AIReportService

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

service = AIReportService(client)

result = service.generate_daily_report()

print("\n========== AI REPORT ==========\n")

print(result["report"])

print("\n========== GENERATED FILES ==========\n")

print(result["pdf"])
print(result["docx"])