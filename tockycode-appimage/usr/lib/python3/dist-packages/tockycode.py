#!/usr/bin/env python3
"""
TockyCode - Professional AI Code Generator
A local AI-powered code generation tool that runs entirely on your machine.
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any
import hashlib
import re

# Try to import optional dependencies
try:
    from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


class TockyCodeEngine:
    """Core AI engine for code generation using local models."""
    
    def __init__(self, model_name: str = "microsoft/CodeGPT-small-py"):
        self.model_name = model_name
        self.generator = None
        self.initialized = False
        
    def initialize(self, force_cpu: bool = False) -> bool:
        """Initialize the local AI model."""
        if not TRANSFORMERS_AVAILABLE:
            print("Installing transformers...")
            subprocess.run([sys.executable, "-m", "pip", "install", "transformers", "torch"], 
                         capture_output=True)
            
        if not TORCH_AVAILABLE:
            print("Error: PyTorch is required. Please install: pip install torch")
            return False
            
        try:
            print(f"Loading model: {self.model_name}...")
            if force_cpu:
                device = "cpu"
            else:
                device = "cuda" if TORCH_AVAILABLE and torch.cuda.is_available() else "cpu"
            
            self.generator = pipeline(
                "text-generation",
                model=self.model_name,
                tokenizer=self.model_name,
                device=-1 if device == "cpu" else 0
            )
            self.initialized = True
            print(f"Model loaded successfully on {device}")
            return True
        except Exception as e:
            print(f"Warning: Could not load primary model: {e}")
            print("Falling back to rule-based code generation...")
            self.initialized = True
            return True
    
    def generate_code(self, prompt: str, language: str = "python", 
                     max_length: int = 500) -> str:
        """Generate code based on prompt."""
        
        if self.generator is None:
            return self._rule_based_generation(prompt, language)
        
        full_prompt = f"# {language} code\n# Task: {prompt}\n```\n"
        
        try:
            result = self.generator(full_prompt, max_length=max_length, 
                                   num_return_sequences=1,
                                   temperature=0.7,
                                   top_p=0.9,
                                   do_sample=True)
            return self._extract_code(result[0]['generated_text'], language)
        except Exception as e:
            print(f"Generation error: {e}, using fallback...")
            return self._rule_based_generation(prompt, language)
    
    def _rule_based_generation(self, prompt: str, language: str) -> str:
        """Fallback rule-based code generation."""
        
        templates = {
            "python": self._python_template,
            "javascript": self._javascript_template,
            "java": self._java_template,
            "cpp": self._cpp_template,
            "go": self._go_template,
            "rust": self._rust_template,
            "typescript": self._typescript_template,
        }
        
        generator = templates.get(language.lower(), self._python_template)
        return generator(prompt)
    
    def _python_template(self, prompt: str) -> str:
        """Generate Python code from prompt."""
        
        prompt_lower = prompt.lower()
        
        # Function generator
        if "function" in prompt_lower or "def" in prompt_lower:
            if "calculate" in prompt_lower or "math" in prompt_lower:
                return '''def calculate_result(value: float) -> float:
    """Calculate result based on input value."""
    import math
    return math.sqrt(abs(value)) * 2


if __name__ == "__main__":
    result = calculate_result(25)
    print(f"Result: {result}")
'''
            elif "string" in prompt_lower or "text" in prompt_lower:
                return '''def process_text(text: str) -> str:
    """Process and transform text."""
    return text.strip().title()


if __name__ == "__main__":
    result = process_text("  hello world  ")
    print(f"Result: {result}")
'''
        
        # Class generator
        if "class" in prompt_lower:
            return '''class DataProcessor:
    """Professional data processor class."""
    
    def __init__(self):
        self.data = []
        self._cache = {}
    
    def add(self, item):
        """Add item to processing queue."""
        self.data.append(item)
        return self
    
    def process(self):
        """Process all items in queue."""
        return [self._transform(item) for item in self.data]
    
    def _transform(self, item):
        """Transform individual item."""
        if isinstance(item, dict):
            return {k: v.upper() if isinstance(v, str) else v for k, v in item.items()}
        return item
    
    def clear(self):
        """Clear all data."""
        self.data.clear()
        self._cache.clear()


if __name__ == "__main__":
    processor = DataProcessor()
    processor.add({"name": "test", "value": 123})
    print(processor.process())
'''
        
        # API/Server generator
        if "api" in prompt_lower or "server" in prompt_lower or "rest" in prompt_lower:
            return '''from flask import Flask, jsonify, request
from typing import Dict, List, Any
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

data_store: List[Dict[str, Any]] = []


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "version": "1.0.0"})


@app.route("/api/data", methods=["GET"])
def get_all_data():
    return jsonify({"data": data_store, "count": len(data_store)})


@app.route("/api/data", methods=["POST"])
def create_data():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    data["id"] = len(data_store) + 1
    data_store.append(data)
    return jsonify({"success": True, "data": data}), 201


@app.route("/api/data/<int:item_id>", methods=["GET"])
def get_data(item_id: int):
    item = next((d for d in data_store if d.get("id") == item_id), None)
    if not item:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"data": item})


@app.route("/api/data/<int:item_id>", methods=["PUT"])
def update_data(item_id: int):
    data = request.get_json()
    for i, item in enumerate(data_store):
        if item.get("id") == item_id:
            data_store[i].update(data)
            return jsonify({"success": True, "data": data_store[i]})
    return jsonify({"error": "Not found"}), 404


@app.route("/api/data/<int:item_id>", methods=["DELETE"])
def delete_data(item_id: int):
    global data_store
    data_store = [d for d in data_store if d.get("id") != item_id]
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
'''
        
        # CLI generator
        if "cli" in prompt_lower or "command" in prompt_lower:
            return '''#!/usr/bin/env python3
"""Professional CLI application."""
import argparse
import sys
from pathlib import Path


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="TockyCode CLI - Professional code generator",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    gen_parser = subparsers.add_parser("generate", help="Generate code")
    gen_parser.add_argument("-p", "--prompt", required=True, help="Code generation prompt")
    gen_parser.add_argument("-l", "--language", default="python", help="Programming language")
    gen_parser.add_argument("-o", "--output", help="Output file path")
    
    ana_parser = subparsers.add_parser("analyze", help="Analyze code")
    ana_parser.add_argument("-f", "--file", required=True, help="File to analyze")
    ana_parser.add_argument("--format", choices=["json", "text"], default="text")
    
    subparsers.add_parser("version", help="Show version information")
    
    return parser


def main():
    parser = setup_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    from tockycode import TockyCodeEngine
    
    engine = TockyCodeEngine()
    engine.initialize()
    
    if args.command == "version":
        print("TockyCode v1.0.0 - Professional AI Code Generator")
        print("Local AI-powered, 100% free")
        return 0
    
    elif args.command == "generate":
        code = engine.generate_code(args.prompt, args.language)
        
        if args.output:
            Path(args.output).write_text(code)
            print(f"Code saved to: {args.output}")
        else:
            print(code)
        return 0
    
    elif args.command == "analyze":
        content = Path(args.file).read_text()
        lines = content.splitlines()
        
        if args.format == "json":
            result = {
                "file": args.file,
                "lines": len(lines),
                "characters": len(content),
            }
            print(json.dumps(result, indent=2))
        else:
            print(f"File: {args.file}")
            print(f"Total lines: {len(lines)}")
            print(f"Characters: {len(content)}")
        return 0
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''
        
        # Database generator
        if "database" in prompt_lower or "sql" in prompt_lower or "db" in prompt_lower:
            return '''import sqlite3
from typing import List, Dict, Any, Optional
from contextlib import contextmanager
import logging

logging.basicConfig(level=logging.INFO)


class DatabaseManager:
    """Professional SQLite database manager."""
    
    def __init__(self, db_path: str = "app.db"):
        self.db_path = db_path
        self._init_database()
    
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def _init_database(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    def create_user(self, username: str, email: str) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email) VALUES (?, ?)",
                (username, email)
            )
            return cursor.lastrowid


if __name__ == "__main__":
    db = DatabaseManager("example.db")
    user_id = db.create_user("john", "john@example.com")
    print(f"Created user with ID: {user_id}")
'''
        
        # Default template
        return '''"""
TockyCode - Professional AI Code Generator
"""
from typing import Any, Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)


class CodeGenerator:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
    
    def generate(self, prompt: str) -> str:
        return f"# Generated code for: {prompt}\\n# Add implementation here"


if __name__ == "__main__":
    generator = CodeGenerator()
    print(generator.generate("hello"))
'''
    
    def _javascript_template(self, prompt: str) -> str:
        return '''/**
 * TockyCode - Professional JavaScript Code Generator
 */

class AppManager {
    constructor() {
        this.data = new Map();
        this.config = { debug: true, maxRetries: 3, timeout: 5000 };
    }

    async initialize() {
        console.log('Initializing...');
        return true;
    }

    async fetchData(url) {
        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });
            return await response.json();
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }
}

export default AppManager;

const app = new AppManager();
app.initialize().then(() => console.log('Ready'));
'''
    
    def _java_template(self, prompt: str) -> str:
        return '''package com.tockycode.app;

import java.util.*;

/**
 * TockyCode - Professional Java Code Generator
 */
public class AppManager {
    private final Map<String, Object> config = new HashMap<>();
    private final List<Object> dataStore = new ArrayList<>();
    
    public AppManager() {
        config.put("debug", true);
        config.put("version", "1.0.0");
    }
    
    public void add(Object item) { dataStore.add(item); }
    public List<Object> getAll() { return new ArrayList<>(dataStore); }
    public int size() { return dataStore.size(); }
    
    public static void main(String[] args) {
        AppManager app = new AppManager();
        app.add("Test");
        System.out.println("Items: " + app.size());
    }
}
'''
    
    def _cpp_template(self, prompt: str) -> str:
        return '''#include <iostream>
#include <memory>
#include <vector>
#include <string>

/**
 * TockyCode - Professional C++ Code Generator
 */
class AppManager {
private:
    std::vector<std::string> data_;
    bool debug_;
public:
    AppManager(bool debug = true) : debug_(debug) {}
    void add(const std::string& item) { data_.push_back(item); }
    size_t size() const { return data_.size(); }
};

int main() {
    auto app = std::make_unique<AppManager>(true);
    app->add("Item");
    std::cout << "Total: " << app->size() << std::endl;
    return 0;
}
'''
    
    def _go_template(self, prompt: str) -> str:
        return '''package main

import (
    "fmt"
    "sync"
)

// TockyCode - Professional Go Code Generator

type AppManager struct {
    data map[string]interface{}
    mu   sync.RWMutex
}

func New() *AppManager {
    return &AppManager{data: make(map[string]interface{})}
}

func (a *AppManager) Set(key string, value interface{}) {
    a.mu.Lock()
    defer a.mu.Unlock()
    a.data[key] = value
}

func (a *AppManager) Get(key string) (interface{}, bool) {
    a.mu.RLock()
    defer a.mu.RUnlock()
    return a.data[key]
}

func main() {
    app := New()
    app.Set("name", "TockyCode")
    fmt.Printf("Name: %v\\n", app.Get("name"))
}
'''
    
    def _rust_template(self, prompt: str) -> str:
        return '''// TockyCode - Professional Rust Code Generator

use std::collections::HashMap;

pub struct AppManager {
    data: HashMap<String, String>,
}

impl AppManager {
    pub fn new() -> Self {
        Self { data: HashMap::new() }
    }
    
    pub fn set(&mut self, key: &str, value: &str) {
        self.data.insert(key.to_string(), value.to_string());
    }
    
    pub fn get(&self, key: &str) -> Option<&String> {
        self.data.get(key)
    }
}

fn main() {
    let mut app = AppManager::new();
    app.set("name", "TockyCode");
    println!("Name: {:?}", app.get("name"));
}
'''
    
    def _typescript_template(self, prompt: str) -> str:
        return '''// TockyCode - Professional TypeScript Code Generator

interface Config {
    debug: boolean;
    maxRetries: number;
    timeout: number;
}

class AppManager {
    private data: Map<string, any> = new Map();
    private config: Config = { debug: true, maxRetries: 3, timeout: 5000 };
    
    set(key: string, value: any): void {
        this.data.set(key, value);
    }
    
    get(key: string): any {
        return this.data.get(key);
    }
}

const app = new AppManager();
app.set("name", "TockyCode");
console.log(app.get("name"));

export { AppManager, Config };
'''
    
    def _extract_code(self, generated_text: str, language: str) -> str:
        if "```" in generated_text:
            start = generated_text.find("```") + 3
            if language:
                start = generated_text.find("\n", start) + 1
            end = generated_text.find("```", start)
            if end > start:
                return generated_text[start:end].strip()
        return generated_text


def main():
    """Main entry point for TockyCode CLI."""
    
    parser = argparse.ArgumentParser(
        description="TockyCode - Professional AI Code Generator (100%% Free, Local)"
    )
    
    parser.add_argument("--version", action="store_true", help="Show version")
    parser.add_argument("--cpu", action="store_true", help="Force CPU mode")
    parser.add_argument("--model", default="microsoft/CodeGPT-small-py", help="AI model")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    gen_parser = subparsers.add_parser("generate", help="Generate code")
    gen_parser.add_argument("-p", "--prompt", required=True, help="Code description")
    gen_parser.add_argument("-l", "--language", default="python", help="Language")
    gen_parser.add_argument("-o", "--output", help="Output file")
    
    ana_parser = subparsers.add_parser("analyze", help="Analyze code")
    ana_parser.add_argument("-f", "--file", required=True, help="File to analyze")
    ana_parser.add_argument("--format", choices=["json", "text"], default="text")
    
    subparsers.add_parser("interactive", help="Interactive mode")
    
    args = parser.parse_args()
    
    if args.version:
        print("TockyCode v1.0.0")
        print("Professional AI Code Generator (100% Free, Local)")
        return 0
    
    if not args.command:
        parser.print_help()
        return 1
    
    engine = TockyCodeEngine(args.model)
    engine.initialize(force_cpu=args.cpu)
    
    if args.command == "generate":
        code = engine.generate_code(args.prompt, args.language)
        
        if args.output:
            Path(args.output).write_text(code)
            print(f"Code saved to: {args.output}")
        else:
            print(code)
            
    elif args.command == "analyze":
        content = Path(args.file).read_text()
        lines = content.splitlines()
        
        if args.format == "json":
            result = {"file": args.file, "lines": len(lines), "characters": len(content)}
            print(json.dumps(result, indent=2))
        else:
            print(f"File: {args.file}")
            print(f"Lines: {len(lines)}")
            print(f"Characters: {len(content)}")
            
    elif args.command == "interactive":
        print("TockyCode Interactive Mode (Ctrl+C to exit)")
        print("=" * 40)
        
        while True:
            try:
                prompt = input("\nDescribe code: ")
                language = input("Language [python]: ") or "python"
                
                code = engine.generate_code(prompt, language)
                print("\n--- Generated Code ---")
                print(code)
                print("--- End ---\n")
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
    
    return 0


if __name__ == "__main__":
    sys.exit(main())