"""
Main entry point for Multi-Agent Chat System
"""
import sys
from core.logger import SystemLogger
from agents.coordinator import Coordinator

def main():
    """Main function to run the multi-agent system"""
    print("=" * 80)
    print("MULTI-AGENT CHAT SYSTEM")
    print("Knowledge Representation & Reasoning Assignment")
    print("=" * 80)
    print()
    
    # Initialize logger
    logger = SystemLogger(console_output=True)
    
    # Initialize coordinator
    coordinator = Coordinator(logger=logger)
    
    print("System initialized. Available agents:")
    print("  - Coordinator (orchestrates all agents)")
    print("  - ResearchAgent (retrieves information)")
    print("  - AnalysisAgent (performs reasoning and analysis)")
    print("  - MemoryAgent (manages system memory)")
    print()
    print("Type 'exit' or 'quit' to end the session")
    print("Type 'status' to view system status")
    print("=" * 80)
    print()
    
    # Interactive loop
    while True:
        try:
            user_input = input("User: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit']:
                print("\nShutting down multi-agent system...")
                break
            
            if user_input.lower() == 'status':
                status = coordinator.get_system_status()
                print(f"\nSystem Status:")
                print(f"  Memory: {status['memory_stats']}")
                print()
                continue
            
            # Process query
            print()
            response = coordinator.process_query(user_input)
            print()
            
        except KeyboardInterrupt:
            print("\n\nInterrupted. Shutting down...")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            print()
    
    print("\nSession ended.")
    print("=" * 80)

if __name__ == "__main__":
    main()
