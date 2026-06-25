import json
import os
from datetime import datetime
import folium

class DataArchiver:
    def __init__(self, output_dir="dispatch_history"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def archive_session(self, optimized_manifest, total_distance):
        """
        Saves a timestamped JSON file of the calculations and generates
        a clean, interactive HTML routing map for deployment.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. Export JSON Analytical Data
        meta_data = {
            "timestamp": datetime.now().isoformat(),
            "total_distance_weight": total_distance,
            "total_stops": len(optimized_manifest),
            "manifest": optimized_manifest
        }
        
        json_path = os.path.exists(f"{self.output_dir}/manifest_{timestamp}.json")
        with open(f"{self.output_dir}/manifest_{timestamp}.json", "w") as f:
            json.dump(meta_data, f, indent=4)

        # 2. Generate Map Visualization (Folium)
        # We base our map center around our starting point (Index 0 / Hub)
        start_lat = optimized_manifest[0]['lat']
        start_lng = optimized_manifest[0]['lng']
        
        route_map = folium.Map(location=[start_lat, start_lng], zoom_start=13, tiles="OpenStreetMap")
        
        # Draw location pins on the map grid
        points = []
        for step, node in enumerate(optimized_manifest):
            lat, lng = node['lat'], node['lng']
            points.append((lat, lng))
            
            p_color = "red" if node.get('priority') == 3 else "blue"
            folium.Marker(
                location=[lat, lng],
                popup=f"Stop {step}: {node['name']} (Priority: {node.get('priority')})",
                icon=folium.Icon(color=p_color, icon="info-sign")
            ).add_to(route_map)

        # Connect the pins with a directional vector line tracking our mathematical path optimization
        folium.PolyLine(points, color="darkgreen", weight=4, opacity=0.8).add_to(route_map)
        
        map_path = f"{self.output_dir}/route_map_{timestamp}.html"
        route_map.save(map_path)
        
        return json_path, map_path