# Round 1B: Persona-Based Section Analyzer (Adobe Hackathon 2025)

import os
import json
import fitz  # PyMuPDF
import time
from datetime import datetime
from typing import List, Dict

class PersonaBasedExtractor:
    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def load_persona_context(self) -> Dict:
        """Loads persona and job-to-be-done context from JSON file."""
        persona_file = os.path.join(self.input_dir, "persona.json")
        try:
            with open(persona_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise RuntimeError(f"Error reading persona.json: {e}")

    def scan_documents(self, pdf_paths: List[str], keywords: List[str]) -> List[Dict]:
        """Scans PDFs and finds relevant sections based on keywords."""
        sections = []
        rank = 1
        for pdf_path in pdf_paths:
            try:
                doc = fitz.open(pdf_path)
                for page_number in range(len(doc)):
                    page = doc[page_number]
                    text = page.get_text().lower()
                    if any(keyword in text for keyword in keywords):
                        snippet = self._extract_relevant_text(text, keywords)
                        sections.append({
                            "document": os.path.basename(pdf_path),
                            "page": page_number + 1,
                            "section_title": f"Relevant Section on Page {page_number + 1}",
                            "importance_rank": rank,
                            "refined_text": snippet
                        })
                        rank += 1
            except Exception as e:
                print(f"Error processing {pdf_path}: {e}")
        return sections

    def _extract_relevant_text(self, text: str, keywords: List[str]) -> str:
        """Returns a brief excerpt from the page that matches the keywords."""
        sentences = text.split('.')
        filtered = [s.strip() for s in sentences if any(k in s for k in keywords)]
        return '. '.join(filtered[:5]) + ('.' if filtered else '')

    def run(self):
        """Main driver: loads context, processes all PDFs, outputs results."""
        start = time.time()
        context = self.load_persona_context()
        keywords = context.get("job_to_be_done", "").lower().split()
        pdf_files = [
            os.path.join(self.input_dir, f)
            for f in os.listdir(self.input_dir)
            if f.lower().endswith(".pdf")
        ]

        result = {
            "metadata": {
                "documents": [os.path.basename(f) for f in pdf_files],
                "persona": context.get("persona", "Unknown"),
                "job_to_be_done": context.get("job_to_be_done", ""),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "sections": self.scan_documents(pdf_files, keywords)
        }

        os.makedirs(self.output_dir, exist_ok=True)
        output_path = os.path.join(self.output_dir, "output.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        print(f"✅ Extraction completed in {time.time() - start:.2f} seconds.")

if __name__ == "__main__":
    INPUT_DIR = "/app/input"
    OUTPUT_DIR = "/app/output"
    extractor = PersonaBasedExtractor(INPUT_DIR, OUTPUT_DIR)
    extractor.run()
