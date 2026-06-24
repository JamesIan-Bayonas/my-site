import os
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Button, RichLog
from rich.table import Table

from core.ai_parser import AIParser
from core.math_engine import MathEngine

class EcoRouteDashboard(App):
    """An advanced Terminal-First TUI Dashboard for our optimization engine."""
    
    CSS = """
    Screen {
        background: #121212;
    }
    #sidebar {
        width: 35%;
        border-right: solid #333333;
        background: #1a1a1a;
        padding: 1;
    }
    #main-content {
        width: 65%;
        padding: 1;
    }
    .panel-title {
        text-style: bold;
        color: #00ff00;
        margin-bottom: 1;
    }
    .raw-box {
        background: #262626;
        color: #cccccc;
        padding: 1;
        height: 12;
        border: dashed #444444;
        margin-bottom: 1;
    }
    #process-btn {
        background: #005f00;
        color: white;
        width: 100%;
        margin-top: 1;
    }
    #process-btn:hover {
        background: #008700;
    }
    """

    TITLE = "♻️ EcoRoute-AI Engine Monitor"
    BINDINGS = [("q", "quit", "Quit System")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Horizontal(
            Vertical(
                Static("📥 INGESTION TARGET (test_input.txt)", classes="panel-title"),
                Static(self.load_raw_log(), id="raw-log-view", classes="raw-box"),
                Button("Execute Dispatch Optimization", id="process-btn", variant="success"),
                id="sidebar"
            ),
            Vertical(
                Static("📊 REAL-TIME HEURISTIC MANIFEST OUTPUT", classes="panel-title"),
                RichLog(id="output-log", highlight=True, markup=True),
                id="main-content"
            )
        )
        yield Footer()

    def load_raw_log(self) -> str:
        if os.path.exists("test_input.txt"):
            with open("test_input.txt", "r") as file:
                return file.read().strip()
        return "Error: test_input.txt not found in workspace root."

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "process-btn":
            log_window = self.query_one("#output-log", RichLog)
            log_window.clear()
            
            log_window.write("[bold yellow][System][/bold yellow] Initializing local AI parser context...")
            
            # 1. Trigger AI Core Extraction
            ai = AIParser(model_name="qwen2.5-coder")
            raw_text = self.load_raw_log()
            extracted_nodes = ai.extract_logistics_data(raw_text)
            
            log_window.write(f"[bold green][AI Core][/bold green] Extracted {len(extracted_nodes)} logical location nodes successfully.")
            
            # 2. Trigger Mathematics Core Optimization
            log_window.write("[bold yellow][System][/bold yellow] Feeding entities into Graph Heuristics Engine...")
            math_engine = MathEngine()
            optimized_manifest, total_cost = math_engine.optimize_route(extracted_nodes)
            
            # 3. Construct a beautiful structural data table inside the terminal
            table = Table(title=f"Optimized Path Manifest (Total Distance Matrix Weight: {total_cost})", expand=True)
            table.add_column("Stop Sequence", justify="center", style="cyan")
            table.add_column("Target Location Name", style="white")
            table.add_column("Coordinates (Lat, Lng)", style="magenta")
            table.add_column("Operational Priority", justify="center")

            for step, node in enumerate(optimized_manifest):
                p_val = node.get('priority', 1)
                p_str = "[bold red]🚨 CRITICAL[/bold red]" if p_val == 3 else "[white]📦 Standard[/white]"
                table.add_row(
                    str(step),
                    node['name'],
                    f"{node['lat']}, {node['lng']}",
                    p_str
                )
            
            log_window.write("\n")
            log_window.write(table)
            log_window.write("\n[bold green]✔ Dispatch Manifest Generation Process Complete.[/bold green]")

if __name__ == "__main__":
    app = EcoRouteDashboard()
    app.run()