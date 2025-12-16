"""
Test scenarios for multi-agent system
Demonstrates all required functionality
"""
import os
import sys
from core.logger import SystemLogger
from agents.coordinator import Coordinator

class ScenarioRunner:
    """
    Runs predefined test scenarios and saves outputs
    """
    
    def __init__(self, output_dir="outputs"):
        """
        Initialize scenario runner
        
        Args:
            output_dir (str): Directory to save outputs
        """
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def run_scenario(self, name, query, output_file):
        """
        Run a single scenario
        
        Args:
            name (str): Scenario name
            query (str): User query
            output_file (str): Output file name
        """
        print(f"\n{'=' * 80}")
        print(f"RUNNING SCENARIO: {name}")
        print(f"{'=' * 80}\n")
        
        # Initialize logger with file output
        log_file = os.path.join(self.output_dir, output_file)
        logger = SystemLogger(log_file=log_file, console_output=True)
        
        # Initialize coordinator
        coordinator = Coordinator(logger=logger)
        
        # Process query
        response = coordinator.process_query(query)
        
        print(f"\n{'=' * 80}")
        print(f"SCENARIO '{name}' COMPLETED")
        print(f"Output saved to: {log_file}")
        print(f"{'=' * 80}\n")
    
    def run_all_scenarios(self):
        """Run all required test scenarios"""
        
        # Scenario 1: Simple Query
        self.run_scenario(
            name="Simple Query",
            query="What are the main types of neural networks?",
            output_file="simple_query.txt"
        )
        
        # Scenario 2: Complex Query
        self.run_scenario(
            name="Complex Query",
            query="Research transformer architectures, analyze their computational efficiency, and summarize key trade-offs.",
            output_file="complex_query.txt"
        )
        
        # Scenario 3: Memory Test
        self.run_scenario(
            name="Memory Test",
            query="What did we discuss about neural networks earlier?",
            output_file="memory_test.txt"
        )
        
        # Scenario 4: Multi-step Query
        self.run_scenario(
            name="Multi-step Query",
            query="Find recent papers on reinforcement learning, analyze their methodologies, and identify common challenges.",
            output_file="multi_step.txt"
        )
        
        # Scenario 5: Collaborative Decision
        self.run_scenario(
            name="Collaborative Decision",
            query="Compare convolutional neural networks and recurrent neural networks and recommend which is better for image processing.",
            output_file="collaborative.txt"
        )

def main():
    """Main function"""
    print("=" * 80)
    print("MULTI-AGENT SYSTEM - TEST SCENARIOS")
    print("Knowledge Representation & Reasoning Assignment")
    print("=" * 80)
    
    runner = ScenarioRunner(output_dir="outputs")
    runner.run_all_scenarios()
    
    print("\n" + "=" * 80)
    print("ALL SCENARIOS COMPLETED")
    print("Check the 'outputs' directory for detailed logs")
    print("=" * 80)

if __name__ == "__main__":
    main()
