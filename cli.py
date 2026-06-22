from core.ai_parser import AIParser
from core.math_engine import MathEngine

def main():
    print("[System Initialize] EcoRoute-AI Engine Active.")
    
    # Simulate receiving unstructured community data
    sample_dispatch = "Hey dispatcher, we need to drop off supplies at Stop A, then head back to the main Hub."
    
    # 1. Initialize Engines
    ai = AIParser()
    math_core = MathEngine()
    
    # 2. Run Pipeline
    print("\n[Step 1] Sending unstructured data to AI parser...")
    structured_data = ai.extract_logistics_data(sample_dispatch)
    print(f" -> AI Extracted Nodes: {structured_data}")
    
    print("\n[Step 2] Sending structured locations to Mathematical Core...")
    optimized_route = math_core.solve_tsp(structured_data)
    print(f" -> Math Optimized Stop Order: {optimized_route}")
    
    print("\n[System Complete] Success.")

if __name__ == "__main__":
    main()