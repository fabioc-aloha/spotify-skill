# Advanced Skill Creation - Examples & Patterns

## Real-World Skill Examples

This document shows complete examples of different skill types to help you understand the patterns.

---

## Example 1: API Wrapper Skill (Like Spotify)

### Structure

```
api-wrapper-skill/
├── SKILL.md
├── scripts/
│   ├── client.py (API wrapper)
│   └── utilities.py (helpers)
└── references/
    ├── authentication.md
    └── api_reference.md
```

### Pattern: API Client Wrapper

**When to use this pattern:**
- Integrating external APIs
- Multiple endpoints to cover
- Authentication required
- Need reusable operations

### SKILL.md Structure

```markdown
---
name: external-api-skill
description: Connect to [Service] API and perform specific operations. 
Handles authentication, pagination, rate limiting.
---

# [Service] API Skill

## Core Capabilities
1. Operation 1
2. Operation 2
3. Operation 3

## Quick Start
[Minimal code]

## Common Workflows
### Workflow 1
[Pattern + example]

### Workflow 2
[Pattern + example]

## References
- references/authentication.md - Setup
- references/api_reference.md - Endpoints
```

### Scripts Pattern

```python
# scripts/client.py
class ServiceClient:
    """Authenticated client for Service API."""
    
    def __init__(self, credentials):
        self.credentials = credentials
        self.token = None
    
    def authenticate(self):
        """Get authentication token."""
        pass
    
    def _request(self, method, endpoint, **kwargs):
        """Make authenticated API request."""
        pass
    
    # Operation 1
    def operation_1(self, param: str) -> Dict:
        pass
    
    # Operation 2
    def operation_2(self, param: str) -> List:
        pass
```

### Key Practices

1. **Token Management**
   - Auto-refresh tokens
   - Handle expiration
   - Secure storage

2. **Error Handling**
   - Catch API errors
   - Rate limit awareness
   - Retry logic

3. **Documentation**
   - Document each method
   - Show common patterns
   - Include examples

---

## Example 2: Document Processing Skill

### Structure

```
document-skill/
├── SKILL.md
├── scripts/
│   ├── document_processor.py
│   └── helpers.py
├── references/
│   └── document_guide.md
└── assets/
    ├── template.docx
    └── example_output.docx
```

### Pattern: Template-Based Processing

**When to use this pattern:**
- Document generation
- File format manipulation
- Template-based output
- Asset management needed

### SKILL.md Structure

```markdown
---
name: document-processor
description: Create, modify, and analyze documents (.docx, .pdf). 
Support for formatting, images, tables, tracked changes, and comments.
---

# Document Processor

## Quick Start
```python
from document_processor import Document

doc = Document()
doc.add_heading("Title")
doc.add_paragraph("Content")
doc.save("output.docx")
```

## Common Workflows
### Create from Template
[Example]

### Add Content
[Example]

### Apply Formatting
[Example]

## References
- references/document_guide.md
```

### Key Practices

1. **Template Management**
   - Store templates in assets/
   - Load without context bloat
   - Document template usage

2. **Batch Operations**
   - Process multiple files
   - Handle errors gracefully
   - Report progress

3. **Quality Output**
   - Preserve formatting
   - Handle edge cases
   - Validate output

---

## Example 3: Multi-Domain Skill

### Structure

```
multi-domain-skill/
├── SKILL.md (overview)
├── scripts/
│   ├── domain1_handler.py
│   ├── domain2_handler.py
│   └── domain3_handler.py
└── references/
    ├── domain1_guide.md
    ├── domain2_guide.md
    └── domain3_guide.md
```

### Pattern: Modular Domain Organization

**When to use this pattern:**
- Multiple distinct domains
- Different operations per domain
- Significant documentation per domain
- Independent workflows

### SKILL.md Structure

```markdown
---
name: multi-domain-system
description: Handle [Domain 1], [Domain 2], and [Domain 3] operations 
with specialized workflows and data management.
---

# Multi-Domain System

## Core Domains

### Domain 1
See references/domain1_guide.md

### Domain 2
See references/domain2_guide.md

### Domain 3
See references/domain3_guide.md

## Quick Start
```python
from domain1_handler import Domain1Handler
from domain2_handler import Domain2Handler

d1 = Domain1Handler()
d2 = Domain2Handler()
```

## Cross-Domain Workflows
[Operations spanning domains]
```

### Key Practices

1. **Clear Boundaries**
   - Each domain has own handler
   - Separate reference docs
   - Minimal cross-domain coupling

2. **Navigation**
   - SKILL.md acts as index
   - Clear "see also" links
   - Easy to find right section

3. **Scalability**
   - Easy to add new domains
   - Each domain can grow independently
   - Organized structure

---

## Example 4: Code Generation Skill

### Structure

```
code-generator-skill/
├── SKILL.md
├── scripts/
│   ├── generator.py
│   └── validators.py
├── references/
│   └── patterns.md
└── assets/
    ├── templates/
    │   ├── react_component.template
    │   ├── python_class.template
    │   └── api_endpoint.template
    └── examples/
        ├── example1.jsx
        └── example2.py
```

### Pattern: Template-Based Code Generation

**When to use this pattern:**
- Code generation
- Project scaffolding
- Boilerplate generation
- Multiple language support

### SKILL.md Structure

```markdown
---
name: code-generator
description: Generate production-ready code for React components, 
Python classes, API endpoints, and more. Includes templates, validation, 
and customization options.
---

# Code Generator

## Supported Templates
- React Components
- Python Classes
- API Endpoints

## Quick Start
```python
from generator import CodeGenerator

gen = CodeGenerator()
code = gen.generate("react_component", name="Button")
print(code)
```

## Generate React Component
[Example usage]

## Generate Python Class
[Example usage]

## Customization
See references/patterns.md for advanced patterns.
```

### Key Practices

1. **Template Management**
   - Store in assets/templates/
   - Clear placeholder naming
   - Version control templates

2. **Validation**
   - Check generated code syntax
   - Validate against standards
   - Provide helpful errors

3. **Customization**
   - Support parameters/options
   - Allow template selection
   - Document all options

---

## Example 5: Learning/Reference Skill

### Structure

```
learning-skill/
├── SKILL.md (overview)
└── references/
    ├── chapter1.md
    ├── chapter2.md
    ├── chapter3.md
    ├── glossary.md
    └── examples.md
```

### Pattern: Educational Content Organization

**When to use this pattern:**
- Teaching a concept
- Structured learning path
- Reference material
- Knowledge base

### SKILL.md Structure

```markdown
---
name: concept-guide
description: Comprehensive guide to [Concept] including fundamentals, 
advanced patterns, real-world examples, and practice exercises.
---

# Concept Guide

## Learning Path
1. Start with fundamentals (references/chapter1.md)
2. Understand advanced patterns (references/chapter2.md)
3. Study real examples (references/examples.md)
4. Refer to glossary as needed (references/glossary.md)

## Quick Overview
[1-2 paragraph summary]

## Key Concepts
[List of main ideas]

## Common Mistakes
[Pitfalls to avoid]

## References
- references/chapter1.md - Fundamentals
- references/chapter2.md - Advanced Topics
- references/examples.md - Real-World Examples
- references/glossary.md - Key Terms
```

### Key Practices

1. **Progressive Disclosure**
   - Fundamentals first
   - Build complexity gradually
   - Reference advanced topics

2. **Accessibility**
   - Clear explanations
   - Visual examples
   - Practical use cases

3. **Navigation**
   - Clear learning path
   - Cross-references
   - Index/glossary

---

## Common Implementation Patterns

### Pattern 1: Factory Pattern

```python
# Used when creating different types of objects
class ResourceFactory:
    @staticmethod
    def create(resource_type: str, **kwargs):
        if resource_type == "type_a":
            return TypeA(**kwargs)
        elif resource_type == "type_b":
            return TypeB(**kwargs)
        else:
            raise ValueError(f"Unknown type: {resource_type}")

# Usage
resource = ResourceFactory.create("type_a", param="value")
```

### Pattern 2: Builder Pattern

```python
# Used for constructing complex objects
class QueryBuilder:
    def __init__(self):
        self.conditions = []
    
    def where(self, condition: str) -> "QueryBuilder":
        self.conditions.append(condition)
        return self
    
    def limit(self, n: int) -> "QueryBuilder":
        self.limit_value = n
        return self
    
    def build(self) -> str:
        query = "SELECT * FROM table"
        if self.conditions:
            query += " WHERE " + " AND ".join(self.conditions)
        if hasattr(self, 'limit_value'):
            query += f" LIMIT {self.limit_value}"
        return query

# Usage
query = (QueryBuilder()
    .where("age > 18")
    .where("status = 'active'")
    .limit(10)
    .build())
```

### Pattern 3: Strategy Pattern

```python
# Used when you have multiple algorithms
from abc import ABC, abstractmethod

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: List) -> List:
        pass

class QuickSort(SortStrategy):
    def sort(self, data: List) -> List:
        # Quick sort implementation
        pass

class MergeSort(SortStrategy):
    def sort(self, data: List) -> List:
        # Merge sort implementation
        pass

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self.strategy = strategy
    
    def execute(self, data: List) -> List:
        return self.strategy.sort(data)

# Usage
data = [3, 1, 4, 1, 5, 9]
sorter = Sorter(QuickSort())
sorted_data = sorter.execute(data)
```

### Pattern 4: Context Manager Pattern

```python
# Used for resource management
from contextlib import contextmanager

@contextmanager
def api_connection(api_key: str):
    client = APIClient(api_key)
    try:
        yield client
    finally:
        client.close()

# Usage
with api_connection("your_api_key") as client:
    data = client.fetch_data()
```

---

## Error Handling Patterns

### Pattern 1: Graceful Degradation

```python
def fetch_data(url: str, timeout: int = 5) -> Dict:
    """Fetch data with fallback."""
    try:
        response = requests.get(url, timeout=timeout)
        return response.json()
    except requests.Timeout:
        logger.warning(f"Timeout fetching {url}")
        return {"status": "timeout", "data": None}
    except requests.ConnectionError:
        logger.warning(f"Connection error for {url}")
        return {"status": "connection_error", "data": None}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"status": "error", "data": None}
```

### Pattern 2: Retry with Exponential Backoff

```python
import time
from functools import wraps

def retry(max_attempts: int = 3, base_delay: int = 1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    delay = base_delay * (2 ** attempt)
                    logger.info(f"Retry attempt {attempt + 1}, waiting {delay}s")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, base_delay=1)
def unstable_operation():
    # Operation that might fail
    pass
```

### Pattern 3: Custom Exceptions

```python
class APIError(Exception):
    """Base API error."""
    pass

class RateLimitError(APIError):
    """Rate limit exceeded."""
    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f"Rate limited. Retry after {retry_after}s")

class AuthenticationError(APIError):
    """Authentication failed."""
    pass

# Usage
try:
    make_api_call()
except RateLimitError as e:
    time.sleep(e.retry_after)
except AuthenticationError:
    refresh_credentials()
except APIError as e:
    logger.error(f"API error: {e}")
```

---

## Documentation Patterns

### Pattern 1: Docstring Format

```python
def complex_operation(param1: str, param2: int, 
                     param3: Optional[List] = None) -> Dict[str, Any]:
    """Brief description of what operation does.
    
    Longer description explaining the purpose, behavior, and 
    any important details about this operation.
    
    Args:
        param1: Description of param1 and constraints
        param2: Description of param2 and valid range
        param3: Optional description. Defaults to None.
    
    Returns:
        Dictionary with keys:
        - 'result': Main result data
        - 'metadata': Operation metadata
        - 'errors': Any non-fatal errors
    
    Raises:
        ValueError: If param2 is not positive
        TypeError: If param1 is not a string
        APIError: If external API call fails
    
    Examples:
        >>> result = complex_operation("test", 42)
        >>> print(result['result'])
        [result data]
    """
    pass
```

### Pattern 2: README Structure for Reference Docs

```markdown
# Topic Name

## Overview
[What is this?]

## Table of Contents
1. [Basics](#basics)
2. [Advanced](#advanced)
3. [Best Practices](#best-practices)
4. [Examples](#examples)

## Basics
[Fundamental concepts]

## Advanced
[Complex patterns]

## Best Practices
[Do's and don'ts]

## Examples
[Real-world usage]

## Common Errors
[Troubleshooting]

## See Also
[Related topics]
```

---

## Performance Optimization Patterns

### Pattern 1: Caching

```python
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=128)
def expensive_operation(param: str) -> str:
    """Cached expensive operation."""
    # Implementation
    pass

# For time-based cache
class TimedCache:
    def __init__(self, ttl_seconds: int = 300):
        self.cache = {}
        self.ttl = ttl_seconds
    
    def get(self, key: str) -> Optional[Any]:
        if key not in self.cache:
            return None
        value, timestamp = self.cache[key]
        if datetime.now() - timestamp > timedelta(seconds=self.ttl):
            del self.cache[key]
            return None
        return value
    
    def set(self, key: str, value: Any):
        self.cache[key] = (value, datetime.now())
```

### Pattern 2: Batch Processing

```python
def process_in_batches(items: List, batch_size: int = 100):
    """Process items in batches to manage memory."""
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        yield process_batch(batch)

# Usage
for results in process_in_batches(large_list, batch_size=50):
    save_results(results)
```

### Pattern 3: Async Operations

```python
import asyncio
from typing import List

async def fetch_all_async(urls: List[str]) -> List[Dict]:
    """Fetch multiple URLs concurrently."""
    tasks = [fetch_url_async(url) for url in urls]
    return await asyncio.gather(*tasks)

async def fetch_url_async(url: str) -> Dict:
    """Fetch single URL asynchronously."""
    # Implementation using aiohttp
    pass

# Usage
results = asyncio.run(fetch_all_async(urls))
```

---

## Testing Patterns

### Pattern 1: Unit Test Structure

```python
import unittest

class TestMyClass(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.obj = MyClass()
    
    def test_method_success(self):
        """Test successful operation."""
        result = self.obj.method("input")
        self.assertEqual(result, "expected")
    
    def test_method_error(self):
        """Test error handling."""
        with self.assertRaises(ValueError):
            self.obj.method(invalid_input)
    
    def tearDown(self):
        """Clean up after tests."""
        self.obj = None

if __name__ == '__main__':
    unittest.main()
```

### Pattern 2: Mock External Services

```python
from unittest.mock import Mock, patch

@patch('requests.get')
def test_api_call(mock_get):
    """Test with mocked external API."""
    mock_get.return_value.json.return_value = {"data": "test"}
    
    result = fetch_api_data()
    
    mock_get.assert_called_once()
    assert result == {"data": "test"}
```

---

## Security Patterns

### Pattern 1: Secure Credential Handling

```python
import os
from typing import Optional

class SecureConfig:
    """Safely load credentials from environment."""
    
    @staticmethod
    def get_credential(name: str, required: bool = True) -> Optional[str]:
        """Get credential from environment.
        
        Args:
            name: Environment variable name
            required: Raise error if not found
        
        Returns:
            Credential value or None
        
        Raises:
            ValueError: If required and not found
        """
        value = os.getenv(name)
        if not value and required:
            raise ValueError(f"Required credential {name} not found")
        return value

# Usage
api_key = SecureConfig.get_credential("API_KEY")
```

### Pattern 2: Input Validation

```python
from typing import Any
import re

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_param(value: Any, param_type: type, 
                  allowed_values: Optional[List] = None) -> bool:
    """Validate parameter value."""
    if not isinstance(value, param_type):
        raise TypeError(f"Expected {param_type}, got {type(value)}")
    
    if allowed_values and value not in allowed_values:
        raise ValueError(f"Value must be one of {allowed_values}")
    
    return True
```

---

## Conclusion

These patterns represent best practices from production systems. Choose the patterns that fit your skill's needs and domain. Remember:

1. **Clarity over cleverness** - Code should be easy to understand
2. **Consistency** - Use patterns consistently throughout
3. **Documentation** - Document why you chose a pattern
4. **Testing** - Validate your implementations
5. **Security** - Always validate inputs and secure credentials

Happy coding! 🚀
