# XCUI Test Case Generator - Architecture

## Overview

The XCUI Test Case Generator is designed with a modular architecture that separates concerns into distinct components: analysis, generation, and orchestration.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User Interface                       │
│                    (CLI / Python API)                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      XCUITestAgent                           │
│                   (Orchestration Layer)                      │
│  • Coordinates analysis and generation                       │
│  • Manages configuration                                     │
│  • Handles file I/O                                          │
└────────┬────────────────────────────────────┬───────────────┘
         │                                    │
         ▼                                    ▼
┌────────────────────────┐         ┌────────────────────────┐
│   SwiftUIAnalyzer      │         │  XCUITestGenerator     │
│   (Analysis Layer)     │         │  (Generation Layer)    │
│                        │         │                        │
│ • Parses Swift code    │         │ • Generates test code  │
│ • Extracts components  │         │ • Creates page objects │
│ • Identifies patterns  │         │ • Formats output       │
└────────────────────────┘         └────────────────────────┘
         │                                    │
         ▼                                    ▼
┌─────────────────────────────────────────────────────────────┐
│                      File System                             │
│              (SwiftUI Source / Test Output)                  │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Analysis Layer (`src/analyzer/`)

#### SwiftUIAnalyzer
**Purpose:** Parse and analyze SwiftUI source code to extract testable components.

**Key Responsibilities:**
- Parse Swift files using regex patterns
- Identify UI components (Button, TextField, etc.)
- Extract state variables and bindings
- Detect navigation flows
- Find accessibility identifiers

**Data Structures:**
```python
@dataclass
class UIComponent:
    type: str                    # Component type (Button, TextField, etc.)
    name: Optional[str]          # Display name/label
    accessibility_id: Optional[str]  # Accessibility identifier
    properties: Dict[str, str]   # Component properties
    actions: List[str]           # Associated actions
    children: List[UIComponent]  # Nested components
    line_number: int            # Source line number

@dataclass
class ViewAnalysis:
    view_name: str              # View struct name
    file_path: str              # Source file path
    components: List[UIComponent]
    state_variables: List[Dict]
    navigation_destinations: List[str]
    bindings: List[Dict]
    environment_objects: List[str]
    imports: List[str]
```

**Analysis Process:**
1. Read Swift file content
2. Extract view name from struct declaration
3. Parse imports and dependencies
4. Identify state management (@State, @Binding, etc.)
5. Scan for UI components using pattern matching
6. Extract component properties and identifiers
7. Detect navigation patterns
8. Return structured analysis result

### 2. Generation Layer (`src/generator/`)

#### XCUITestGenerator
**Purpose:** Generate XCUI test code from analysis results.

**Key Responsibilities:**
- Generate test methods for UI interactions
- Create navigation tests
- Generate validation tests
- Create accessibility tests
- Generate page object classes
- Format code with proper Swift syntax

**Test Generation Strategy:**

```python
def generate_tests(analysis: ViewAnalysis) -> str:
    """
    1. Generate UI interaction tests
       - Button taps
       - Text input
       - Toggle switches
       - Picker selections
    
    2. Generate navigation tests
       - NavigationLink destinations
       - Sheet presentations
       - Alert handling
    
    3. Generate validation tests
       - Form validation
       - Input constraints
       - Error states
    
    4. Generate accessibility tests
       - Identifier presence
       - VoiceOver support
       - Dynamic type
    
    5. Build complete test file
       - Add imports
       - Create test class
       - Add setup/teardown
       - Include all test methods
    """
```

**Code Templates:**

The generator uses templates for consistent code generation:

```swift
// Button Test Template
func test_{name}_ButtonTap() {
    // Given: The {view} is displayed
    let app = XCUIApplication()
    app.launch()
    
    // When: User taps the {name} button
    let button = app.buttons["{identifier}"]
    XCTAssertTrue(button.exists)
    button.tap()
    
    // Then: Verify expected action
    // TODO: Add specific assertion
}
```

### 3. Orchestration Layer (`src/agent/`)

#### XCUITestAgent
**Purpose:** Coordinate the entire test generation process.

**Key Responsibilities:**
- Load and manage configuration
- Initialize analyzer and generator
- Orchestrate analysis workflow
- Manage file output
- Provide high-level API
- Handle errors and logging

**Workflow:**

```python
def generate_tests(views: Optional[List[str]] = None):
    """
    1. Load configuration
    2. Scan project for Swift files
    3. Filter by view names (if specified)
    4. For each view:
       a. Analyze SwiftUI code
       b. Generate test cases
       c. Generate page objects (if enabled)
       d. Write to output files
    5. Return summary of generated files
    """
```

### 4. Utility Layer (`src/utils/`)

#### File Utilities
- Find Swift files in directory
- Read/write file content
- Manage directory structure
- Handle path operations

## Data Flow

### Analysis Flow
```
Swift Source File
    ↓
Read File Content
    ↓
Extract View Structure
    ↓
Parse UI Components
    ↓
Identify Patterns
    ↓
ViewAnalysis Object
```

### Generation Flow
```
ViewAnalysis Object
    ↓
Identify Testable Components
    ↓
Generate Test Methods
    ↓
Apply Code Templates
    ↓
Format Swift Code
    ↓
Test File String
```

### End-to-End Flow
```
User Request
    ↓
XCUITestAgent.generate_tests()
    ↓
SwiftUIAnalyzer.analyze_project()
    ↓
For each view:
    SwiftUIAnalyzer.analyze_file()
        ↓
    XCUITestGenerator.generate_tests()
        ↓
    Write to file system
    ↓
Return generated file paths
```

## Configuration System

### Configuration Hierarchy
1. Default configuration (hardcoded)
2. Config file (config/agent_config.yaml)
3. Custom config file (--config parameter)
4. Runtime overrides (Python API)

### Configuration Structure
```yaml
analysis:
  file_extensions: [".swift"]
  exclude_patterns: ["*Tests.swift"]
  components_to_track: [Button, TextField, ...]

generation:
  test_framework: "XCTest"
  include_setup_teardown: true
  generate_page_objects: true
  naming_convention: "descriptive"

output:
  create_separate_files: true
  file_naming: "{view_name}UITests.swift"
  include_comments: true

llm:
  provider: "openai"
  model: "gpt-4"
  temperature: 0.3
```

## Extension Points

### 1. Custom Analyzers
Extend `SwiftUIAnalyzer` to add custom analysis:

```python
class CustomAnalyzer(SwiftUIAnalyzer):
    def analyze_custom_pattern(self, content: str):
        # Custom analysis logic
        pass
```

### 2. Custom Generators
Extend `XCUITestGenerator` for custom test generation:

```python
class CustomGenerator(XCUITestGenerator):
    def generate_custom_tests(self, analysis: ViewAnalysis):
        # Custom generation logic
        pass
```

### 3. LLM Integration
Future enhancement for intelligent test generation:

```python
class LLMEnhancedAgent(XCUITestAgent):
    def generate_intelligent_tests(self, analysis: ViewAnalysis):
        # Use LLM to generate contextual tests
        # Understand business logic
        # Generate edge cases
        pass
```

## Design Patterns

### 1. Strategy Pattern
Different test generation strategies can be swapped:
- Basic generation
- LLM-enhanced generation
- Template-based generation

### 2. Builder Pattern
Test code is built incrementally:
- Add imports
- Add class structure
- Add setup/teardown
- Add test methods

### 3. Factory Pattern
Component-specific test generators:
- ButtonTestFactory
- TextFieldTestFactory
- NavigationTestFactory

### 4. Page Object Pattern
Generated page objects encapsulate UI elements:
- Centralized element definitions
- Reusable actions
- Better maintainability

## Performance Considerations

### 1. File Parsing
- Use efficient regex patterns
- Cache parsed results
- Process files in parallel (future)

### 2. Code Generation
- Template-based generation is fast
- Minimal string operations
- Batch file writes

### 3. Memory Usage
- Stream large files
- Process one view at a time
- Clean up after each view

## Testing Strategy

### Unit Tests
- Test analyzer pattern matching
- Test generator templates
- Test utility functions

### Integration Tests
- Test full analysis pipeline
- Test generation pipeline
- Test file I/O operations

### End-to-End Tests
- Test with real SwiftUI projects
- Verify generated tests compile
- Verify generated tests run

## Future Enhancements

### 1. LLM Integration
- Use GPT-4/Claude for intelligent test generation
- Generate contextual test descriptions
- Suggest edge cases
- Generate test data

### 2. Advanced Analysis
- Use tree-sitter for proper AST parsing
- Support complex SwiftUI patterns
- Detect custom components
- Analyze view models

### 3. Test Execution
- Run generated tests automatically
- Report test results
- Suggest improvements

### 4. CI/CD Integration
- GitHub Actions workflow
- Automatic test generation on PR
- Test coverage reporting

### 5. IDE Integration
- Xcode extension
- VS Code extension
- Real-time test generation