# XCUI Test Case Generator Agent

An intelligent agent that automatically generates XCUI test cases for iOS SwiftUI projects by analyzing your SwiftUI code structure and UI components.

## Features

- 🔍 **SwiftUI Code Analysis**: Parses SwiftUI views to identify UI components, navigation flows, and user interactions
- 🤖 **AI-Powered Generation**: Uses LLM to generate comprehensive XCUI test cases
- 📝 **Best Practices**: Generates test cases following Apple's XCUI testing guidelines
- 🎯 **Accessibility-First**: Leverages accessibility identifiers for robust test selectors
- 🔄 **Incremental Updates**: Can update existing test suites when code changes

## Project Structure

```
XCUI_TestCase_Agent/
├── src/
│   ├── analyzer/          # SwiftUI code analysis modules
│   ├── generator/         # XCUI test case generation
│   ├── agent/            # Main agent orchestration
│   └── utils/            # Utility functions
├── tests/                # Unit tests
├── examples/             # Example SwiftUI projects
├── config/               # Configuration files
└── docs/                 # Documentation
```

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd XCUI_TestCase_Agent

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```python
from src.agent.xcui_agent import XCUITestAgent

# Initialize the agent
agent = XCUITestAgent(
    project_path="path/to/your/swiftui/project",
    output_path="path/to/output/tests"
)

# Generate test cases
agent.generate_tests()
```

## Usage

### Basic Usage

```python
# Analyze a single SwiftUI file
from src.analyzer.swiftui_analyzer import SwiftUIAnalyzer

analyzer = SwiftUIAnalyzer()
analysis = analyzer.analyze_file("ContentView.swift")

# Generate test cases
from src.generator.test_generator import XCUITestGenerator

generator = XCUITestGenerator()
test_code = generator.generate_tests(analysis)
```

### Advanced Usage

```python
# Configure the agent with custom settings
agent = XCUITestAgent(
    project_path="./MyApp",
    output_path="./MyAppUITests",
    config={
        "include_accessibility_tests": True,
        "generate_performance_tests": True,
        "test_naming_convention": "test_<feature>_<action>_<expected>"
    }
)

# Generate tests for specific views
agent.generate_tests(views=["LoginView", "ProfileView"])
```

## Configuration

Create a `config/agent_config.yaml` file:

```yaml
analysis:
  file_extensions: [".swift"]
  exclude_patterns: ["*Tests.swift", "*.generated.swift"]
  
generation:
  test_framework: "XCTest"
  include_setup_teardown: true
  generate_page_objects: true
  
llm:
  provider: "openai"
  model: "gpt-4"
  temperature: 0.3
```

## Examples

See the `examples/` directory for complete examples:
- Simple login form
- Navigation flow testing
- List and detail view testing
- Form validation testing

## Contributing

Contributions are welcome! Please read our contributing guidelines.

## License

MIT License