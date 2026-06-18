"""
XCUI Test Case Generator
Generates XCUI test cases from SwiftUI analysis results.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from ..analyzer.swiftui_analyzer import ViewAnalysis, UIComponent


@dataclass
class TestCase:
    """Represents a generated test case"""
    name: str
    description: str
    code: str
    test_type: str  # ui_interaction, navigation, validation, accessibility


class XCUITestGenerator:
    """Generates XCUI test cases from analyzed SwiftUI views"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.indent = " " * self.config.get('indent_size', 4)
    
    def generate_tests(self, analysis: ViewAnalysis) -> str:
        """Generate complete test file for a view"""
        test_cases = []
        
        # Generate UI interaction tests
        test_cases.extend(self._generate_interaction_tests(analysis))
        
        # Generate navigation tests
        if analysis.navigation_destinations:
            test_cases.extend(self._generate_navigation_tests(analysis))
        
        # Generate validation tests
        if analysis.state_variables:
            test_cases.extend(self._generate_validation_tests(analysis))
        
        # Generate accessibility tests
        test_cases.extend(self._generate_accessibility_tests(analysis))
        
        # Build complete test file
        return self._build_test_file(analysis, test_cases)
    
    def _generate_interaction_tests(self, analysis: ViewAnalysis) -> List[TestCase]:
        """Generate tests for UI interactions"""
        tests = []
        
        for component in analysis.components:
            if component.type == 'Button':
                test = self._generate_button_test(component, analysis.view_name)
                if test:
                    tests.append(test)
            
            elif component.type in ['TextField', 'SecureField']:
                test = self._generate_textfield_test(component, analysis.view_name)
                if test:
                    tests.append(test)
            
            elif component.type == 'Toggle':
                test = self._generate_toggle_test(component, analysis.view_name)
                if test:
                    tests.append(test)
        
        return tests
    
    def _generate_button_test(self, component: UIComponent, view_name: str) -> Optional[TestCase]:
        """Generate test for button tap"""
        if not component.accessibility_id and not component.name:
            return None
        
        identifier = component.accessibility_id or component.name or "unknown"
        safe_name = self._sanitize_name(identifier)
        
        code = f"""
{self.indent}func test_{safe_name}_ButtonTap() {{
{self.indent * 2}// Given: The {view_name} is displayed
{self.indent * 2}let app = XCUIApplication()
{self.indent * 2}app.launch()
{self.indent * 2}
{self.indent * 2}// When: User taps the {identifier} button
{self.indent * 2}let button = app.buttons["{identifier}"]
{self.indent * 2}XCTAssertTrue(button.exists, "{identifier} button should exist")
{self.indent * 2}button.tap()
{self.indent * 2}
{self.indent * 2}// Then: Verify the expected action occurred
{self.indent * 2}// TODO: Add specific assertion for button action
{self.indent}}}
"""
        
        return TestCase(
            name=f"test_{safe_name}_ButtonTap",
            description=f"Test tapping the {identifier} button",
            code=code.strip(),
            test_type="ui_interaction"
        )
    
    def _generate_textfield_test(self, component: UIComponent, view_name: str) -> Optional[TestCase]:
        """Generate test for text field input"""
        if not component.accessibility_id and not component.name:
            return None
        
        identifier = component.accessibility_id or component.name or "unknown"
        safe_name = self._sanitize_name(identifier)
        is_secure = component.type == 'SecureField'
        element_type = "secureTextFields" if is_secure else "textFields"
        
        code = f"""
{self.indent}func test_{safe_name}_TextInput() {{
{self.indent * 2}// Given: The {view_name} is displayed
{self.indent * 2}let app = XCUIApplication()
{self.indent * 2}app.launch()
{self.indent * 2}
{self.indent * 2}// When: User enters text in {identifier}
{self.indent * 2}let textField = app.{element_type}["{identifier}"]
{self.indent * 2}XCTAssertTrue(textField.exists, "{identifier} text field should exist")
{self.indent * 2}textField.tap()
{self.indent * 2}textField.typeText("Test Input")
{self.indent * 2}
{self.indent * 2}// Then: Verify text was entered
{self.indent * 2}XCTAssertEqual(textField.value as? String, "Test Input")
{self.indent}}}
"""
        
        return TestCase(
            name=f"test_{safe_name}_TextInput",
            description=f"Test entering text in {identifier}",
            code=code.strip(),
            test_type="ui_interaction"
        )
    
    def _generate_toggle_test(self, component: UIComponent, view_name: str) -> Optional[TestCase]:
        """Generate test for toggle switch"""
        if not component.accessibility_id and not component.name:
            return None
        
        identifier = component.accessibility_id or component.name or "unknown"
        safe_name = self._sanitize_name(identifier)
        
        code = f"""
{self.indent}func test_{safe_name}_Toggle() {{
{self.indent * 2}// Given: The {view_name} is displayed
{self.indent * 2}let app = XCUIApplication()
{self.indent * 2}app.launch()
{self.indent * 2}
{self.indent * 2}// When: User toggles the {identifier} switch
{self.indent * 2}let toggle = app.switches["{identifier}"]
{self.indent * 2}XCTAssertTrue(toggle.exists, "{identifier} toggle should exist")
{self.indent * 2}
{self.indent * 2}let initialValue = toggle.value as? String
{self.indent * 2}toggle.tap()
{self.indent * 2}
{self.indent * 2}// Then: Verify toggle state changed
{self.indent * 2}let newValue = toggle.value as? String
{self.indent * 2}XCTAssertNotEqual(initialValue, newValue, "Toggle state should change")
{self.indent}}}
"""
        
        return TestCase(
            name=f"test_{safe_name}_Toggle",
            description=f"Test toggling {identifier}",
            code=code.strip(),
            test_type="ui_interaction"
        )
    
    def _generate_navigation_tests(self, analysis: ViewAnalysis) -> List[TestCase]:
        """Generate tests for navigation flows"""
        tests = []
        
        for destination in analysis.navigation_destinations:
            safe_name = self._sanitize_name(destination)
            
            code = f"""
{self.indent}func test_NavigationTo_{safe_name}() {{
{self.indent * 2}// Given: The {analysis.view_name} is displayed
{self.indent * 2}let app = XCUIApplication()
{self.indent * 2}app.launch()
{self.indent * 2}
{self.indent * 2}// When: User navigates to {destination}
{self.indent * 2}// TODO: Add specific navigation action (e.g., tap button/link)
{self.indent * 2}
{self.indent * 2}// Then: Verify {destination} is displayed
{self.indent * 2}// TODO: Add assertion to verify destination view
{self.indent * 2}XCTAssertTrue(app.navigationBars["{destination}"].exists)
{self.indent}}}
"""
            
            tests.append(TestCase(
                name=f"test_NavigationTo_{safe_name}",
                description=f"Test navigation to {destination}",
                code=code.strip(),
                test_type="navigation"
            ))
        
        return tests
    
    def _generate_validation_tests(self, analysis: ViewAnalysis) -> List[TestCase]:
        """Generate tests for form validation"""
        tests = []
        
        # Check if there are text fields that might need validation
        text_components = [c for c in analysis.components if c.type in ['TextField', 'SecureField']]
        
        if text_components:
            code = f"""
{self.indent}func test_{analysis.view_name}_FormValidation() {{
{self.indent * 2}// Given: The {analysis.view_name} is displayed
{self.indent * 2}let app = XCUIApplication()
{self.indent * 2}app.launch()
{self.indent * 2}
{self.indent * 2}// When: User submits form with invalid data
{self.indent * 2}// TODO: Enter invalid data in form fields
{self.indent * 2}
{self.indent * 2}// Then: Verify validation errors are shown
{self.indent * 2}// TODO: Add assertions for validation messages
{self.indent}}}
"""
            
            tests.append(TestCase(
                name=f"test_{analysis.view_name}_FormValidation",
                description=f"Test form validation in {analysis.view_name}",
                code=code.strip(),
                test_type="validation"
            ))
        
        return tests
    
    def _generate_accessibility_tests(self, analysis: ViewAnalysis) -> List[TestCase]:
        """Generate accessibility tests"""
        tests = []
        
        # Test that all interactive elements have accessibility identifiers
        code = f"""
{self.indent}func test_{analysis.view_name}_AccessibilityIdentifiers() {{
{self.indent * 2}// Given: The {analysis.view_name} is displayed
{self.indent * 2}let app = XCUIApplication()
{self.indent * 2}app.launch()
{self.indent * 2}
{self.indent * 2}// Then: Verify all interactive elements have accessibility identifiers
"""
        
        for component in analysis.components:
            if component.accessibility_id:
                element_type = self._get_xcui_element_type(component.type)
                code += f"""
{self.indent * 2}XCTAssertTrue(app.{element_type}["{component.accessibility_id}"].exists,
{self.indent * 3}"{component.accessibility_id} should have accessibility identifier")
"""
        
        code += f"{self.indent}}}"
        
        tests.append(TestCase(
            name=f"test_{analysis.view_name}_AccessibilityIdentifiers",
            description=f"Test accessibility identifiers in {analysis.view_name}",
            code=code.strip(),
            test_type="accessibility"
        ))
        
        return tests
    
    def _build_test_file(self, analysis: ViewAnalysis, test_cases: List[TestCase]) -> str:
        """Build complete test file with imports and class structure"""
        class_name = f"{analysis.view_name}UITests"
        
        header = f"""//
//  {class_name}.swift
//  Generated by XCUI Test Case Generator
//
//  Test cases for {analysis.view_name}
//

import XCTest

class {class_name}: XCTestCase {{
    
    var app: XCUIApplication!
    
    override func setUpWithError() throws {{
        continueAfterFailure = false
        app = XCUIApplication()
    }}
    
    override func tearDownWithError() throws {{
        app = nil
    }}
"""
        
        # Add all test cases
        test_methods = "\n\n".join([tc.code for tc in test_cases])
        
        footer = "\n}\n"
        
        return header + "\n" + test_methods + footer
    
    def _sanitize_name(self, name: str) -> str:
        """Sanitize name for use in test method names"""
        # Remove special characters and spaces
        sanitized = ''.join(c if c.isalnum() else '_' for c in name)
        # Remove consecutive underscores
        sanitized = '_'.join(filter(None, sanitized.split('_')))
        return sanitized
    
    def _get_xcui_element_type(self, component_type: str) -> str:
        """Map SwiftUI component type to XCUI element type"""
        mapping = {
            'Button': 'buttons',
            'TextField': 'textFields',
            'SecureField': 'secureTextFields',
            'Toggle': 'switches',
            'Text': 'staticTexts',
            'Image': 'images',
            'NavigationLink': 'buttons',
        }
        return mapping.get(component_type, 'otherElements')
    
    def generate_page_object(self, analysis: ViewAnalysis) -> str:
        """Generate Page Object pattern class for the view"""
        class_name = f"{analysis.view_name}Page"
        
        code = f"""//
//  {class_name}.swift
//  Page Object for {analysis.view_name}
//

import XCTest

class {class_name} {{
    
    let app: XCUIApplication
    
    init(app: XCUIApplication) {{
        self.app = app
    }}
    
    // MARK: - Elements
"""
        
        # Add element properties
        for component in analysis.components:
            if component.accessibility_id or component.name:
                identifier = component.accessibility_id or component.name or "unknown"
                safe_name = self._sanitize_name(identifier)
                element_type = self._get_xcui_element_type(component.type)
                
                code += f"""
{self.indent}var {safe_name}: XCUIElement {{
{self.indent * 2}return app.{element_type}["{identifier}"]
{self.indent}}}
"""
        
        code += f"""
    
    // MARK: - Actions
    
{self.indent}func waitForView() -> Bool {{
{self.indent * 2}return app.navigationBars["{analysis.view_name}"].waitForExistence(timeout: 5)
{self.indent}}}
}}
"""
        
        return code

# Made with Bob
