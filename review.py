import os
import openai
from datetime import datetime

openai.api_key = "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"

# Supported file types
SUPPORTED_EXTENSIONS = [
    ".py", ".json", ".sql", ".js", ".ts", ".html", ".css",
    ".yaml", ".yml", ".md", ".txt"
]

def read_files(folder_path):
    """Scan folder recursively and read supported file types."""
    collected_files = {}

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        collected_files[filepath] = f.read()
                except Exception:
                    collected_files[filepath] = "⚠️ Could not read file due to encoding or permission issues."

    return collected_files


def ai_review_file(filepath, content):
    """Generate AI review for file content."""
    prompt = f"""
You are an expert multi-language code reviewer. Analyze the following file content and provide:
1. ✅ Summary of what the file does  
2. ✅ Code quality issues  
3. ✅ Security issues  
4. ✅ Logical bugs  
5. ✅ Performance concerns  
6. ✅ Best practices per language  
7. ✅ Suggested improvements  
8. ✅ Risk score (Low, Medium, High)  

FILE: {filepath}
CONTENT:
{content}
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "You are an expert code reviewer skilled in multiple programming languages."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        return response.choices[0].message["content"]

    except Exception as e:
        return f"❌ AI review failed: {e}"


def generate_markdown_report(reviews):
    """Write results to markdown file."""
    report_name = "ai_multi_file_code_review_report.md"
    
    with open(report_name, "w", encoding="utf-8") as report:
        report.write("# 🤖 Multi-File AI Code Review Report\n")
        report.write(f"Generated on: **{datetime.now()}**\n")
        report.write("\n---\n")

        for filepath, review in reviews.items():
            report.write(f"## 📄 File: `{filepath}`\n\n")
            report.write(review + "\n\n")
            report.write("\n---\n")

    print(f"\n✅ Review generated successfully: {report_name}")


if __name__ == "__main__":
    print("\n=== Multi-File AI Code Review Tool ===\n")

    folder = input("Enter folder path (leave empty for current directory): ").strip()

    if folder == "":
        folder = "."

    if not os.path.exists(folder):
        print("❌ Error: Path does not exist.")
        exit()

    print(f"\n📁 Scanning: {os.path.abspath(folder)}\n")

    files = read_files(folder)

    if not files:
        print("⚠️ No supported files found.")
        exit()

    print(f"✅ Found {len(files)} files. Starting AI review...\n")

    reviews = {}
    for filepath, content in files.items():
        print(f"🔍 Reviewing: {filepath}")
        reviews[filepath] = ai_review_file(filepath, content)

    generate_markdown_report(reviews)

    print("\n✅ Done.")
