"""
SwiftUI Code Analyzer
Analyzes SwiftUI code to extract UI components, structure, and interactions.
"""

import re
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class UIComponent:
    """Represents a UI component in SwiftUI"""
    type: str
    name: Optional[str] = None
    accessibility_id: Optional[str] = None
    properties: Dict[str, str] = field(default_factory=dict)
    actions: List[str] = field(default_factory=list)
    children: List['UIComponent'] = field(default_factory=list)
    line_number: int = 0


@dataclass
class ViewAnalysis:
    """Analysis result for a SwiftUI view"""
    view_name: str
    file_path: str
    components: List[UIComponent]
    state_variables: List[Dict[str, str]]
    navigation_destinations: List[str]
    bindings: List[Dict[str, str]]
    environment_objects: List[str]
    imports: List[str]


class SwiftUIAnalyzer:
    """Analyzes SwiftUI code to extract testable components"""
    
    # SwiftUI component patterns
    COMPONENT_PATTERNS = {
        'Button': r'Button\s*\(',
        'TextField': r'TextField\s*\(',
        'SecureField': r'SecureField\s*\(',
        'Toggle': r'Toggle\s*\(',
        'Picker': r'Picker\s*\(',
        'Slider': r'Slider\s*\(',
        'Stepper': r'Stepper\s*\(',
        'NavigationLink': r'NavigationLink\s*\(',
        'List': r'List\s*\{',
        'Form': r'Form\s*\{',
        'TabView': r'TabView\s*\{',
        'Text': r'Text\s*\(',
        'Image': r'Image\s*\(',
    }
    
    def __init__(self):
        self.current_file: Optional[str] = None
        self.current_view: Optional[str] = None
    
    def analyze_file(self, file_path: str) -> ViewAnalysis:
        """Analyze a SwiftUI file and extract components"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.current_file = file_path
        
        # Extract view name
        view_name = self._extract_view_name(content)
        self.current_view = view_name
        
        # Extract imports
        imports = self._extract_imports(content)
        
        # Extract state variables
        state_vars = self._extract_state_variables(content)
        
        # Extract environment objects
        env_objects = self._extract_environment_objects(content)
        
        # Extract bindings
        bindings = self._extract_bindings(content)
        
        # Extract UI components
        components = self._extract_components(content)
        
        # Extract navigation destinations
        nav_destinations = self._extract_navigation_destinations(content)
        
        return ViewAnalysis(
            view_name=view_name,
            file_path=file_path,
            components=components,
            state_variables=state_vars,
            navigation_destinations=nav_destinations,
            bindings=bindings,
            environment_objects=env_objects,
            imports=imports
        )
    
    def _extract_view_name(self, content: str) -> str:
        """Extract the main view name from the file"""
        # Look for struct ViewName: View pattern
        match = re.search(r'struct\s+(\w+)\s*:\s*View', content)
        if match:
            return match.group(1)
        return "UnknownView"
    
    def _extract_imports(self, content: str) -> List[str]:
        """Extract import statements"""
        imports = []
        for match in re.finditer(r'import\s+(\w+)', content):
            imports.append(match.group(1))
        return imports
    
    def _extract_state_variables(self, content: str) -> List[Dict[str, str]]:
        """Extract @State, @StateObject, @ObservedObject variables"""
        state_vars = []
        
        patterns = [
            (r'@State\s+(?:private\s+)?var\s+(\w+)\s*:\s*([^\s=]+)', 'State'),
            (r'@StateObject\s+(?:private\s+)?var\s+(\w+)\s*:\s*([^\s=]+)', 'StateObject'),
            (r'@ObservedObject\s+(?:private\s+)?var\s+(\w+)\s*:\s*([^\s=]+)', 'ObservedObject'),
            (r'@Binding\s+var\s+(\w+)\s*:\s*([^\s=]+)', 'Binding'),
        ]
        
        for pattern, var_type in patterns:
            for match in re.finditer(pattern, content):
                state_vars.append({
                    'name': match.group(1),
                    'type': match.group(2),
                    'decorator': var_type
                })
        
        return state_vars
    
    def _extract_environment_objects(self, content: str) -> List[str]:
        """Extract @EnvironmentObject variables"""
        env_objects = []
        pattern = r'@EnvironmentObject\s+var\s+(\w+)\s*:\s*(\w+)'
        for match in re.finditer(pattern, content):
            env_objects.append(f"{match.group(1)}: {match.group(2)}")
        return env_objects
    
    def _extract_bindings(self, content: str) -> List[Dict[str, str]]:
        """Extract binding relationships"""
        bindings = []
        # Look for $variable patterns
        for match in re.finditer(r'\$(\w+)', content):
            bindings.append({
                'variable': match.group(1),
                'type': 'two-way'
            })
        return bindings
    
    def _extract_components(self, content: str) -> List[UIComponent]:
        """Extract UI components from the view body"""
        components = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for comp_type, pattern in self.COMPONENT_PATTERNS.items():
                if re.search(pattern, line):
                    component = self._parse_component(line, comp_type, line_num, content)
                    if component:
                        components.append(component)
        
        return components
    
    def _parse_component(self, line: str, comp_type: str, line_num: int, full_content: str) -> Optional[UIComponent]:
        """Parse a component line to extract details"""
        component = UIComponent(type=comp_type, line_number=line_num)
        
        # Extract text/label for buttons and text fields
        text_match = re.search(r'["\']([^"\']+)["\']', line)
        if text_match:
            component.name = text_match.group(1)
        
        # Extract accessibility identifier
        acc_id_match = re.search(r'\.accessibilityIdentifier\s*\(\s*["\']([^"\']+)["\']\s*\)', line)
        if acc_id_match:
            component.accessibility_id = acc_id_match.group(1)
        
        # Extract actions for buttons
        if comp_type == 'Button':
            action_match = re.search(r'action:\s*\{([^}]+)\}', line)
            if action_match:
                component.actions.append('tap')
        
        # Extract binding for text fields
        if comp_type in ['TextField', 'SecureField', 'Toggle']:
            binding_match = re.search(r'text:\s*\$(\w+)', line)
            if binding_match:
                component.properties['binding'] = binding_match.group(1)
        
        return component
    
    def _extract_navigation_destinations(self, content: str) -> List[str]:
        """Extract navigation destinations"""
        destinations = []
        
        # NavigationLink destinations
        for match in re.finditer(r'NavigationLink\s*\([^)]*destination:\s*(\w+)', content):
            destinations.append(match.group(1))
        
        # Sheet presentations
        for match in re.finditer(r'\.sheet\s*\([^)]*content:\s*\{\s*(\w+)', content):
            destinations.append(match.group(1))
        
        return destinations
    
    def analyze_project(self, project_path: str) -> List[ViewAnalysis]:
        """Analyze all SwiftUI files in a project"""
        project = Path(project_path)
        analyses = []
        
        # Find all .swift files
        swift_files = list(project.rglob("*.swift"))
        
        for swift_file in swift_files:
            # Skip test files
            if 'Test' in swift_file.name:
                continue
            
            try:
                analysis = self.analyze_file(str(swift_file))
                analyses.append(analysis)
            except Exception as e:
                print(f"Error analyzing {swift_file}: {e}")
        
        return analyses
    
    def get_testable_components(self, analysis: ViewAnalysis) -> List[UIComponent]:
        """Filter components that are testable (have accessibility IDs or clear identifiers)"""
        testable = []
        
        for component in analysis.components:
            # Components with accessibility IDs are always testable
            if component.accessibility_id:
                testable.append(component)
            # Components with names/labels are testable
            elif component.name:
                testable.append(component)
            # Interactive components are testable
            elif component.type in ['Button', 'TextField', 'SecureField', 'Toggle', 'NavigationLink']:
                testable.append(component)
        
        return testable

# Made with Bob
