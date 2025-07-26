# Team_SMS_Round_1B– Persona-Based Document Analyzer

## 🧠 Objective
This project builds an intelligent system that scans multiple PDFs and identifies relevant sections based on a given persona and job-to-be-done. It complies with the Adobe Hackathon Round 1B requirements.

## 📥 Input Specification
- **PDF files**: Place 3–10 domain-related PDFs in `/app/input`
- **persona.json** file with the following structure:
```json
{
  "persona": "Investment Analyst",
  "job_to_be_done": "Analyze revenue trends and R&D investments"
}
```

## 📤 Output Specification
- A single JSON file `/app/output/output.json` containing:
  - Metadata
    - List of documents
    - Persona and job description
    - Processing timestamp
  - Extracted sections:
    - File name
    - Page number
    - Matched section title
    - Importance rank
    - Refined matching text (up to 5 sentences)

### ✅ Sample Output JSON Format
```json
{
  "metadata": {
    "documents": ["report1.pdf", "report2.pdf"],
    "persona": "Investment Analyst",
    "job_to_be_done": "Analyze revenue trends and R&D investments",
    "timestamp": "2025-07-26 18:45:00"
  },
  "sections": [
    {
      "document": "report1.pdf",
      "page": 3,
      "section_title": "Relevant Section on Page 3",
      "importance_rank": 1,
      "refined_text": "Company revenue increased by 20%..."
    }
  ]
}
```

## 🐳 Docker Instructions
### 🏗 Build Docker Image
```bash
docker build --platform linux/amd64 -t persona_analyzer:round1b .
```

### ▶ Run the Container
```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none persona_analyzer:round1b
```


## ✅ Constraints Satisfied
- CPU-only, AMD64 architecture
- Runs offline (no internet required)
- Executes within 60 seconds for 3–5 PDFs
- No external APIs or oversized models

## 🧠 Approach Summary
The script identifies relevant content based on simple keyword matching from the job-to-be-done string. Pages containing matching content are extracted, ranked, and summarized into a compact JSON format.

---

Crafted for Adobe India Hackathon 2025 🚀
