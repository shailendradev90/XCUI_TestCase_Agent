# XCUI Test Case Generator - Usage Guide

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Command Line Interface](#command-line-interface)
4. [Python API](#python-api)
5. [Configuration](#configuration)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites
- Python 3.8 or higher
- iOS/SwiftUI project with accessibility identifiers

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd XCUI_TestCase_Agent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file (optional, for LLM features)
cp .env.example .env
# Edit .env and add your API keys
```

## Quick Start

### Generate Tests for Your Project

```bash
# Basic usage
python main.py --project /path/to/your/swiftui/project --output ./UITests

# Generate tests for specific views
python main.py --project ./MyApp --output ./MyAppUITests --views LoginView ProfileView

# View project summary first
python main.py --project ./MyApp --summary
```

### Example Output

```
🚀 Initializing XCUI Test Agent...
🔍 Analyzing SwiftUI project at: ./MyApp
✅ Found 5 SwiftUI views

📝 Generating tests for LoginView...
   ✅ Generated: ./UITests/LoginViewUITests.swift
   ✅ Generated Page Object: ./UITests/PageObjects/LoginViewPage.swift

🎉 Test generation complete! Generated 5 test files
```

## Command Line Interface

### Available Commands

#### Generate Tests
```bash
python main.py --project <path> --output <path> [options]
```

**Options:**
- `--project, -p`: Path to SwiftUI project (required)
- `--output, -o`: Output directory for tests (default: ./UITests)
- `--config, -c`: Path to config file (default: config/agent_config.yaml)
- `--views, -v`: Specific views to test (space-separated)

#### Project Summary
```bash
python main.py --project <path> --summary
```

Shows:
- Total number of views
- Total UI components
- Testable components
- Component breakdown by type

#### Test Report
```bash
python main.py --project <path> --report
```

Generates a detailed report of what tests will be created.

## Python API

### Basic Usage

```python
from src.agent.xcui_agent import XCUITestAgent

# Initialize agent
agent = XCUITestAgent(
    project_path="./MyApp",
    output_path="./MyAppUITests"
)

# Generate all tests
agent.generate_tests()
```

### Advanced Usage

```python
from src.agent.xcui_agent import XCUITestAgent
from src.analyzer.swiftui_analyzer import SwiftUIAnalyzer
from src.generator.test_generator import XCUITestGenerator

# Custom configuration
agent = XCUITestAgent(
    project_path="./MyApp",
    output_path="./MyAppUITests",
    config_path="./custom_config.yaml"
)

# Generate tests for specific views
agent.generate_tests(views=["LoginView", "ProfileView"])

# Analyze a single view
analysis = agent.analyze_view("./MyApp/Views/LoginView.swift")
print(f"Found {len(analysis.components)} components")

# Get project summary
summary = agent.get_project_summary()
print(f"Total views: {summary['total_views']}")
print(f"Testable components: {summary['testable_components']}")

# Generate test for single view
test_file = agent.generate_test_for_view("./MyApp/Views/LoginView.swift")
print(f"Generated: {test_file}")
```

### Using Individual Components

```python
# Analyzer only
from src.analyzer.swiftui_analyzer import SwiftUIAnalyzer

analyzer = SwiftUIAnalyzer()
analysis = analyzer.analyze_file("LoginView.swift")

print(f"View: {analysis.view_name}")
print(f"Components: {len(analysis.components)}")
print(f"State variables: {analysis.state_variables}")

# Generator only
from src.generator.test_generator import XCUITestGenerator

generator = XCUITestGenerator()
test_code = generator.generate_tests(analysis)
page_object = generator.generate_page_object(analysis)
```

## Configuration

### Configuration File Structure

```yaml
# config/agent_config.yaml

analysis:
  file_extensions: [".swift"]
  exclude_patterns: ["*Tests.swift"]
  components_to_track:
    - Button
    - TextField
    - Toggle
    # ... more components

generation:
  test_framework: "XCTest"
  include_setup_teardown: true
  generate_page_objects: true
  naming_convention: "descriptive"
  
  test_types:
    - ui_interaction
    - navigation
    - validation
    - accessibility

output:
  create_separate_files: true
  file_naming: "{view_name}UITests.swift"
  include_comments: true
```

### Customizing Test Generation

```python
config = {
    'generation': {
        'indent_size': 4,
        'include_setup_teardown': True,
        'generate_page_objects': True
    }
}

agent = XCUITestAgent(
    project_path="./MyApp",
    output_path="./UITests",
    config_path=None  # Use dict instead
)
agent.config = config
```

## Best Practices

### 1. Add Accessibility Identifiers

Always add accessibility identifiers to your SwiftUI views:

```swift
Button("Login") {
    login()
}
.accessibilityIdentifier("loginButton")

TextField("Username", text: $username)
    .accessibilityIdentifier("usernameField")
```

### 2. Organize Your Views

Keep views in a clear directory structure:
```
MyApp/
├── Views/
│   ├── Authentication/
│   │   ├── LoginView.swift
│   │   └── SignUpView.swift
│   └── Profile/
│       └── ProfileView.swift
```

### 3. Review Generated Tests

Always review and customize generated tests:
- Add specific assertions
- Include edge cases
- Add test data
- Update TODO comments

### 4. Use Page Objects

Enable page object generation for better test maintainability:

```swift
// Generated Page Object
class LoginViewPage {
    let app: XCUIApplication
    
    var usernameField: XCUIElement {
        return app.textFields["usernameField"]
    }
    
    var loginButton: XCUIElement {
        return app.buttons["loginButton"]
    }
}

// Use in tests
func testLogin() {
    let loginPage = LoginViewPage(app: app)
    loginPage.usernameField.tap()
    loginPage.usernameField.typeText("testuser")
    loginPage.loginButton.tap()
}
```

### 5. Incremental Generation

Generate tests incrementally as you develop:

```bash
# Generate tests for new view
python main.py --project ./MyApp --output ./UITests --views NewFeatureView
```

## Troubleshooting

### Common Issues

#### 1. No Views Found

**Problem:** Agent reports "No SwiftUI views found"

**Solutions:**
- Verify project path is correct
- Check that files have `.swift` extension
- Ensure views conform to `View` protocol
- Check exclude patterns in config

#### 2. Missing Components

**Problem:** Some UI components not detected

**Solutions:**
- Add accessibility identifiers
- Check component is in `components_to_track` list
- Verify SwiftUI syntax is correct

#### 3. Import Errors

**Problem:** Python import errors

**Solutions:**
```bash
# Ensure you're in project root
cd XCUI_TestCase_Agent

# Reinstall dependencies
pip install -r requirements.txt

# Check Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### 4. Generated Tests Don't Compile

**Problem:** Swift compilation errors

**Solutions:**
- Review accessibility identifiers match
- Update element types (buttons, textFields, etc.)
- Add missing imports in test file
- Verify Xcode project setup

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

agent = XCUITestAgent(project_path="./MyApp", output_path="./UITests")
```

### Getting Help

1. Check the [FAQ](FAQ.md)
2. Review [examples](../examples/)
3. Open an issue on GitHub
4. Check configuration file syntax

## Next Steps

- Read [Advanced Features](ADVANCED_FEATURES.md)
- Explore [Examples](../examples/)
- Learn about [LLM Integration](LLM_INTEGRATION.md)
- Contribute to the project