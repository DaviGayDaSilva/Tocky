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
            func_name = "generated_function"
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


# Usage example
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

# In-memory data store
data_store: List[Dict[str, Any]] = []


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "version": "1.0.0"})


@app.route("/api/data", methods=["GET"])
def get_all_data():
    """Retrieve all data."""
    return jsonify({"data": data_store, "count": len(data_store)})


@app.route("/api/data", methods=["POST"])
def create_data():
    """Create new data entry."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    data["id"] = len(data_store) + 1
    data_store.append(data)
    return jsonify({"success": True, "data": data}), 201


@app.route("/api/data/<int:item_id>", methods=["GET"])
def get_data(item_id: int):
    """Retrieve specific data by ID."""
    item = next((d for d in data_store if d.get("id") == item_id), None)
    if not item:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"data": item})


@app.route("/api/data/<int:item_id>", methods=["PUT"])
def update_data(item_id: int):
    """Update existing data."""
    data = request.get_json()
    for i, item in enumerate(data_store):
        if item.get("id") == item_id:
            data_store[i].update(data)
            return jsonify({"success": True, "data": data_store[i]})
    return jsonify({"error": "Not found"}), 404


@app.route("/api/data/<int:item_id>", methods=["DELETE"])
def delete_data(item_id: int):
    """Delete data by ID."""
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
    """Configure argument parser."""
    parser = argparse.ArgumentParser(
        description="TockyCode CLI - Professional code generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s generate --prompt "function to calculate fibonacci"
  %(prog)s analyze --file main.py
  %(prog)s --version
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate code")
    gen_parser.add_argument("-p", "--prompt", required=True, help="Code generation prompt")
    gen_parser.add_argument("-l", "--language", default="python", help="Programming language")
    gen_parser.add_argument("-o", "--output", help="Output file path")
    
    # Analyze command  
    ana_parser = subparsers.add_parser("analyze", help="Analyze code")
    ana_parser.add_argument("-f", "--file", required=True, help="File to analyze")
    ana_parser.add_argument("--format", choices=["json", "text"], default="text")
    
    # Version command
    subparsers.add_parser("version", help="Show version information")
    
    return parser


def generate_code(prompt: str, language: str, output: str = None):
    """Generate code from prompt."""
    from tockycode import TockyCodeEngine
    
    engine = TockyCodeEngine()
    engine.initialize()
    code = engine.generate_code(prompt, language)
    
    if output:
        Path(output).write_text(code)
        print(f"Code saved to: {output}")
    else:
        print(code)


def analyze_code(file_path: str, format: str = "text"):
    """Analyze code file."""
    content = Path(file_path).read_text()
    
    if format == "json":
        result = {
            "file": file_path,
            "lines": len(content.splitlines()),
            "characters": len(content),
            "functions": len([l for l in content.splitlines() if "def " in l]),
            "classes": len([l for l in content.splitlines() if "class " in l])
        }
        print(json.dumps(result, indent=2))
    else:
        print(f"File: {file_path}")
        print(f"Lines: {len(content.splitlines())}")
        print(f"Characters: {len(content)}")


def main():
    """Main entry point."""
    parser = setup_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    if args.command == "version":
        print("TockyCode v1.0.0 - Professional AI Code Generator")
        print("Local AI-powered, 100%% free")
        return 0
    
    elif args.command == "generate":
        generate_code(args.prompt, args.language, args.output)
        return 0
    
    elif args.command == "analyze":
        analyze_code(args.file, args.format)
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
logger = logging.getLogger(__name__)


class DatabaseManager:
    """Professional SQLite database manager."""
    
    def __init__(self, db_path: str = "app.db"):
        self.db_path = db_path
        self._init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()
    
    def _init_database(self):
        """Initialize database schema."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Products table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL NOT NULL,
                    stock INTEGER DEFAULT 0,
                    category_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories(id)
                )
            """)
            
            # Categories table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT
                )
            """)
            
            logger.info("Database initialized successfully")
    
    def create_user(self, username: str, email: str, password: str) -> int:
        """Create new user."""
        import hashlib
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )
            return cursor.lastrowid
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def list_products(self, category_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """List all products, optionally filtered by category."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if category_id:
                cursor.execute("SELECT * FROM products WHERE category_id = ?", (category_id,))
            else:
                cursor.execute("SELECT * FROM products")
            return [dict(row) for row in cursor.fetchall()]


# Usage example
if __name__ == "__main__":
    db = DatabaseManager("example.db")
    user_id = db.create_user("john", "john@example.com", "password123")
    print(f"Created user with ID: {user_id}")
'''
        
        # Default template
        return '''"""
TockyCode - Professional AI Code Generator
Generated code from local AI model
"""
from typing import Any, Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CodeGenerator:
    """Professional code generator class."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self._initialized = True
        logger.info("CodeGenerator initialized")
    
    def generate(self, prompt: str) -> str:
        """Generate code from prompt."""
        logger.info(f"Generating code for: {prompt}")
        return f"# Generated code for: {prompt}\\n# Add your implementation here"
    
    def validate(self, code: str) -> bool:
        """Validate generated code."""
        return bool(code and len(code) > 0)
    
    def optimize(self, code: str) -> str:
        """Optimize generated code."""
        # Basic optimization
        lines = [line for line in code.split("\\n") if line.strip()]
        return "\\n".join(lines)


if __name__ == "__main__":
    generator = CodeGenerator()
    result = generator.generate("hello world")
    print(result)
'''
    
    def _javascript_template(self, prompt: str) -> str:
        """Generate JavaScript code from prompt."""
        
        return '''/**
 * TockyCode - Professional JavaScript Code Generator
 */

class AppManager {
    constructor() {
        this.data = new Map();
        this.config = {
            debug: true,
            maxRetries: 3,
            timeout: 5000
        };
    }

    async initialize() {
        console.log('Initializing application...');
        this.setupEventListeners();
        return true;
    }

    setupEventListeners() {
        document.addEventListener('DOMContentLoaded', () => {
            console.log('DOM ready');
        });
    }

    async fetchData(url) {
        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            return await response.json();
        } catch (error) {
            console.error('Fetch error:', error);
            throw error;
        }
    }

    processItems(items) {
        return items.map(item => ({
            ...item,
            processed: true,
            timestamp: Date.now()
        }));
    }
}

// Export for module usage
export default AppManager;

// Usage
const app = new AppManager();
app.initialize().then(() => console.log('App ready'));
'''
    
    def _java_template(self, prompt: str) -> str:
        """Generate Java code from prompt."""
        
        return '''package com.tockycode.app;

import java.util.*;
import java.util.stream.*;

/**
 * TockyCode - Professional Java Code Generator
 */
public class AppManager {
    
    private final Map<String, Object> config;
    private final List<Object> dataStore;
    
    public AppManager() {
        this.config = new HashMap<>();
        this.dataStore = new ArrayList<>();
        initialize();
    }
    
    private void initialize() {
        config.put("debug", true);
        config.put("version", "1.0.0");
    }
    
    public void add(Object item) {
        dataStore.add(item);
    }
    
    public List<Object> getAll() {
        return new ArrayList<>(dataStore);
    }
    
    public Optional<Object> find(Predicate<Object> predicate) {
        return dataStore.stream().filter(predicate).findFirst();
    }
    
    public void clear() {
        dataStore.clear();
    }
    
    public int size() {
        return dataStore.size();
    }
    
    public static void main(String[] args) {
        AppManager app = new AppManager();
        app.add("Test Item");
        System.out.println("Items: " + app.size());
    }
}
'''
    
    def _cpp_template(self, prompt: str) -> str:
        """Generate C++ code from prompt."""
        
        return '''#include <iostream>
#include <memory>
#include <vector>
#include <string>
#include <optional>
#include <algorithm>

/**
 * TockyCode - Professional C++ Code Generator
 */
class AppManager {
private:
    std::vector<std::string> data_;
    bool debug_;

public:
    AppManager(bool debug = true) : debug_(debug) {
        if (debug_) std::cout << "AppManager initialized\\n";
    }
    
    void add(const std::string& item) {
        data_.push_back(item);
    }
    
    void remove(const std::string& item) {
        data_.erase(
            std::remove(data_.begin(), data_.end(), item),
            data_.end()
        );
    }
    
    [[nodiscard]] std::vector<std::string> getAll() const {
        return data_;
    }
    
    [[nodiscard]] size_t size() const {
        return data_.size();
    }
    
    void clear() {
        data_.clear();
    }
    
    ~AppManager() {
        if (debug_) std::cout << "AppManager destroyed\\n";
    }
};

int main() {
    auto app = std::make_unique<AppManager>(true);
    app->add("Item 1");
    app->add("Item 2");
    
    std::cout << "Total items: " << app->size() << "\\n";
    
    return 0;
}
'''
    
    def _go_template(self, prompt: str) -> str:
        """Generate Go code from prompt."""
        
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
    return &AppManager{
        data: make(map[string]interface{}),
    }
}

func (a *AppManager) Set(key string, value interface{}) {
    a.mu.Lock()
    defer a.mu.Unlock()
    a.data[key] = value
}

func (a *AppManager) Get(key string) (interface{}, bool) {
    a.mu.RLock()
    defer a.mu.RUnlock()
    val, ok := a.data[key]
    return val, ok
}

func (a *AppManager) Delete(key string) {
    a.mu.Lock()
    defer a.mu.Unlock()
    delete(a.data, key)
}

func (a *AppManager) Keys() []string {
    a.mu.RLock()
    defer a.mu.RUnlock()
    
    keys := make([]string, 0, len(a.data))
    for k := range a.data {
        keys = append(keys, k)
    }
    return keys
}

func main() {
    app := New()
    app.Set("name", "TockyCode")
    app.Set("version", 1.0)
    
    fmt.Printf("Name: %v\\n", app.Get("name"))
    fmt.Printf("Keys: %v\\n", app.Keys())
}
'''
    
    def _rust_template(self, prompt: str) -> str:
        """Generate Rust code from prompt."""
        
        return '''// TockyCode - Professional Rust Code Generator

use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::thread;

#[derive(Debug, Clone)]
pub struct AppManager {
    data: Arc<Mutex<HashMap<String, String>>>,
}

impl AppManager {
    pub fn new() -> Self {
        Self {
            data: Arc::new(Mutex::new(HashMap::new())),
        }
    }
    
    pub fn set(&self, key: impl Into<String>, value: impl Into<String>) {
        let mut data = self.data.lock().unwrap();
        data.insert(key.into(), value.into());
    }
    
    pub fn get(&self, key: &str) -> Option<String> {
        let data = self.data.lock().unwrap();
        data.get(key).cloned()
    }
    
    pub fn remove(&self, key: &str) -> Option<String> {
        let mut data = self.data.lock().unwrap();
        data.remove(key)
    }
    
    pub fn keys(&self) -> Vec<String> {
        let data = self.data.lock().unwrap();
        data.keys().cloned().collect()
    }
    
    pub fn clear(&self) {
        let mut data = self.data.lock().unwrap();
        data.clear();
    }
}

fn main() {
    let app = AppManager::new();
    
    app.set("name", "TockyCode");
    app.set("version", "1.0.0");
    
    println!("Name: {:?}", app.get("name"));
    println!("Keys: {:?}", app.keys());
    
    // Multi-threaded example
    let app_clone = Arc::new(AppManager::new());
    
    let handles: Vec<_> = (0..3)
        .map(|i| {
            let app = Arc::clone(&app_clone);
            thread::spawn(move || {
                app.set(&format!("key_{}", i), &format!("value_{}", i));
            })
        })
        .collect();
    
    for handle in handles {
        handle.join().unwrap();
    }
}
'''
    
    def _typescript_template(self, prompt: str) -> str:
        """Generate TypeScript code from prompt."""
        
        return '''// TockyCode - Professional TypeScript Code Generator

interface Config {
    debug: boolean;
    maxRetries: number;
    timeout: number;
}

interface DataItem {
    id: string;
    name: string;
    value: number;
    timestamp: number;
}

class AppManager<T extends DataItem> {
    private data: Map<string, T> = new Map();
    private config: Config;
    
    constructor(config: Partial<Config> = {}) {
        this.config = {
            debug: true,
            maxRetries: 3,
            timeout: 5000,
            ...config
        };
    }
    
    set(key: string, item: T): void {
        this.data.set(key, item);
    }
    
    get(key: string): T | undefined {
        return this.data.get(key);
    }
    
    has(key: string): boolean {
        return this.data.has(key);
    }
    
    delete(key: string): boolean {
        return this.data.delete(key);
    }
    
    clear(): void {
        this.data.clear();
    }
    
    getAll(): T[] {
        return Array.from(this.data.values());
    }
    
    filter(predicate: (item: T) => boolean): T[] {
        return this.getAll().filter(predicate);
    }
    
    map<U>(transform: (item: T) => U): U[] {
        return this.getAll().map(transform);
    }
}

// Generic function example
function createAppManager<T extends DataItem>(
    items: T[] = [],
    config?: Partial<Config>
): AppManager<T> {
    const app = new AppManager<T>(config);
    items.forEach(item => app.set(item.id, item));
    return app;
}

// Usage example
const app = createAppManager([
    { id: "1", name: "Item 1", value: 100, timestamp: Date.now() },
    { id: "2", name: "Item 2", value: 200, timestamp: Date.now() }
]);

console.log(app.get("1"));
console.log(app.filter(item => item.value > 100));

export { AppManager, createAppManager, Config, DataItem };
'''
    
    def _extract_code(self, generated_text: str, language: str) -> str:
        """Extract code from generated text."""
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
        description="TockyCode - Professional AI Code Generator (100%% Free, Local)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  tockycode generate -p "create a function to calculate fibonacci"
  tockycode generate -p "create REST API with Flask" -l python -o api.py
  tockycode analyze -f main.py
  tockycode --version
        """
    )
    
    parser.add_argument("--version", action="store_true", help="Show version")
    parser.add_argument("--cpu", action="store_true", help="Force CPU mode (no GPU)")
    parser.add_argument("--model", default="microsoft/CodeGPT-small-py", 
                       help="AI model to use")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate code")
    gen_parser.add_argument("-p", "--prompt", required=True, help="Code description")
    gen_parser.add_argument("-l", "--language", default="python", 
                           choices=["python", "javascript", "java", "cpp", "go", 
                                   "rust", "typescript", "c", "csharp", "ruby", 
                                   "php", "swift", "kotlin"],
                           help="Programming language")
    gen_parser.add_argument("-o", "--output", help="Output file")
    gen_parser.add_argument("--max-length", type=int, default=500, 
                            help="Max code length")
    
    # Analyze command
    ana_parser = subparsers.add_parser("analyze", help="Analyze code")
    ana_parser.add_argument("-f", "--file", required=True, help="File to analyze")
    ana_parser.add_argument("--format", choices=["json", "text"], default="text")
    
    # Interactive mode
    subparsers.add_parser("interactive", help="Interactive code generation")
    
    args = parser.parse_args()
    
    if args.version:
        print("TockyCode v1.0.0")
        print("Professional AI Code Generator (100% Free, Local)")
        print("Powered by local AI models")
        return 0
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Initialize engine
    engine = TockyCodeEngine(args.model)
    engine.initialize(force_cpu=args.cpu)
    
    if args.command == "generate":
        code = engine.generate_code(args.prompt, args.language, args.max_length)
        
        if args.output:
            Path(args.output).write_text(code)
            print(f"✓ Code saved to: {args.output}")
        else:
            print(code)
            
    elif args.command == "analyze":
        content = Path(args.file).read_text()
        lines = content.splitlines()
        
        if args.format == "json":
            result = {
                "file": args.file,
                "lines": len(lines),
                "characters": len(content),
                "blank_lines": sum(1 for l in lines if not l.strip()),
                "code_lines": sum(1 for l in lines if l.strip()),
            }
            print(json.dumps(result, indent=2))
        else:
            print(f"File: {args.file}")
            print(f"Total lines: {len(lines)}")
            print(f"Characters: {len(content)}")
            print(f"Blank lines: {sum(1 for l in lines if not l.strip())}")
            
    elif args.command == "interactive":
        print("TockyCode Interactive Mode (Ctrl+C to exit)")
        print("=" * 40)
        
        while True:
            try:
                prompt = input("\nDescribe what you want to code: ")
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