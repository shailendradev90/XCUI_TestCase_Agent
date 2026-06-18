"""
XCUI Test Case Generator Agent
Main orchestrator for analyzing SwiftUI code and generating XCUI tests.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from ..analyzer.swiftui_analyzer import SwiftUIAnalyzer, ViewAnalysis
from ..generator.test_generator import XCUITestGenerator


class XCUITestAgent:
    """Main agent for generating XCUI test cases from SwiftUI projects"""
    
    def __init__(
        self,
        project_path: str,
        output_path: str,
        config_path: Optional[str] = None
    ):
        """
        Initialize the XCUI Test Agent
        
        Args:
            project_path: Path to the SwiftUI project
            output_path: Path where test files will be generated
            config_path: Optional path to configuration file
        """
        self.project_path = Path(project_path)
        self.output_path = Path(output_path)
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize components
        self.analyzer = SwiftUIAnalyzer()
        self.generator = XCUITestGenerator(self.config.get('generation', {}))
        
        # Ensure output directory exists
        self.output_path.mkdir(parents=True, exist_ok=True)
    
    def _load_config(self, config_path: Optional[str] = None) -> Dict:
        """Load configuration from file or use defaults"""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        
        # Try to load from default location
        default_config = Path(__file__).parent.parent.parent / "config" / "agent_config.yaml"
        if default_config.exists():
            with open(default_config, 'r') as f:
                return yaml.safe_load(f)
        
        # Return default configuration
        return {
            'analysis': {
                'file_extensions': ['.swift'],
                'exclude_patterns': ['*Tests.swift', '*UITests.swift']
            },
            'generation': {
                'test_framework': 'XCTest',
                'include_setup_teardown': True,
                'generate_page_objects': True
            }
        }
    
    def generate_tests(self, views: Optional[List[str]] = None) -> Dict[str, str]:
        """
        Generate XCUI test cases for the project
        
        Args:
            views: Optional list of specific view names to generate tests for
        
        Returns:
            Dictionary mapping view names to generated test file paths
        """
        print(f"🔍 Analyzing SwiftUI project at: {self.project_path}")
        
        # Analyze the project
        analyses = self.analyzer.analyze_project(str(self.project_path))
        
        if not analyses:
            print("⚠️  No SwiftUI views found in the project")
            return {}
        
        print(f"✅ Found {len(analyses)} SwiftUI views")
        
        # Filter views if specified
        if views:
            analyses = [a for a in analyses if a.view_name in views]
            print(f"📋 Generating tests for {len(analyses)} specified views")
        
        generated_files = {}
        
        for analysis in analyses:
            print(f"\n📝 Generating tests for {analysis.view_name}...")
            
            try:
                # Generate test file
                test_code = self.generator.generate_tests(analysis)
                test_file_path = self._save_test_file(analysis.view_name, test_code)
                generated_files[analysis.view_name] = str(test_file_path)
                print(f"   ✅ Generated: {test_file_path}")
                
                # Generate page object if configured
                if self.config.get('generation', {}).get('generate_page_objects', False):
                    page_object_code = self.generator.generate_page_object(analysis)
                    page_object_path = self._save_page_object(analysis.view_name, page_object_code)
                    print(f"   ✅ Generated Page Object: {page_object_path}")
                
            except Exception as e:
                print(f"   ❌ Error generating tests for {analysis.view_name}: {e}")
        
        print(f"\n🎉 Test generation complete! Generated {len(generated_files)} test files")
        return generated_files
    
    def _save_test_file(self, view_name: str, content: str) -> Path:
        """Save generated test file"""
        filename = f"{view_name}UITests.swift"
        file_path = self.output_path / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return file_path
    
    def _save_page_object(self, view_name: str, content: str) -> Path:
        """Save generated page object file"""
        page_objects_dir = self.output_path / "PageObjects"
        page_objects_dir.mkdir(exist_ok=True)
        
        filename = f"{view_name}Page.swift"
        file_path = page_objects_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return file_path
    
    def analyze_view(self, view_file: str) -> ViewAnalysis:
        """
        Analyze a specific SwiftUI view file
        
        Args:
            view_file: Path to the SwiftUI view file
        
        Returns:
            ViewAnalysis object containing the analysis results
        """
        return self.analyzer.analyze_file(view_file)
    
    def generate_test_for_view(self, view_file: str) -> str:
        """
        Generate XCUI tests for a specific view file
        
        Args:
            view_file: Path to the SwiftUI view file
        
        Returns:
            Path to the generated test file
        """
        analysis = self.analyze_view(view_file)
        test_code = self.generator.generate_tests(analysis)
        test_file_path = self._save_test_file(analysis.view_name, test_code)
        
        return str(test_file_path)
    
    def get_project_summary(self) -> Dict:
        """
        Get a summary of the project structure
        
        Returns:
            Dictionary containing project statistics
        """
        analyses = self.analyzer.analyze_project(str(self.project_path))
        
        total_components = sum(len(a.components) for a in analyses)
        total_testable = sum(len(self.analyzer.get_testable_components(a)) for a in analyses)
        
        component_types = {}
        for analysis in analyses:
            for component in analysis.components:
                component_types[component.type] = component_types.get(component.type, 0) + 1
        
        return {
            'total_views': len(analyses),
            'total_components': total_components,
            'testable_components': total_testable,
            'component_breakdown': component_types,
            'views': [a.view_name for a in analyses]
        }
    
    def generate_test_report(self) -> str:
        """
        Generate a report of what tests would be generated
        
        Returns:
            Formatted report string
        """
        summary = self.get_project_summary()
        
        report = f"""
XCUI Test Generation Report
{'=' * 50}

Project: {self.project_path.name}
Total Views: {summary['total_views']}
Total Components: {summary['total_components']}
Testable Components: {summary['testable_components']}

Component Breakdown:
"""
        
        for comp_type, count in sorted(summary['component_breakdown'].items()):
            report += f"  - {comp_type}: {count}\n"
        
        report += f"\nViews to be tested:\n"
        for view in summary['views']:
            report += f"  - {view}\n"
        
        return report


class LLMEnhancedAgent(XCUITestAgent):
    """
    Enhanced agent that uses LLM to generate more intelligent test cases
    This is a placeholder for future LLM integration
    """
    
    def __init__(
        self,
        project_path: str,
        output_path: str,
        config_path: Optional[str] = None,
        llm_provider: str = "openai",
        api_key: Optional[str] = None
    ):
        super().__init__(project_path, output_path, config_path)
        self.llm_provider = llm_provider
        self.api_key = api_key or os.getenv(f"{llm_provider.upper()}_API_KEY")
    
    def generate_intelligent_tests(self, analysis: ViewAnalysis) -> str:
        """
        Use LLM to generate more contextual and intelligent test cases
        
        This method would integrate with OpenAI/Anthropic APIs to:
        1. Understand the business logic from code
        2. Generate edge cases
        3. Create more meaningful test descriptions
        4. Suggest test data
        """
        # TODO: Implement LLM integration
        # For now, fall back to standard generation
        return self.generator.generate_tests(analysis)

# Made with Bob
