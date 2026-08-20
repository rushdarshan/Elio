import json
import os
import sys
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unihack_catalog.category_extractors import CATEGORY_TRIGGERS, EXTRACTORS
from unihack_catalog.reference_loader import TAXONOMY_KEYWORDS, BRAND_VOCAB


def main():
    nodes = []
    edges = []
    node_set = set()

    def add_node(node_id, label, group, details=""):
        if node_id not in node_set:
            nodes.append({
                "id": node_id,
                "label": label,
                "group": group,
                "title": details or label
            })
            node_set.add(node_id)

    def add_edge(from_id, to_id, label=""):
        # Avoid duplicate edges
        edge_key = (from_id, to_id, label)
        edges.append({
            "from": from_id,
            "to": to_id,
            "label": label
        })

    # 1. Process Category Triggers & Extractors
    for cat_name, triggers in CATEGORY_TRIGGERS.items():
        extractor_id = f"ext_{cat_name}"
        add_node(extractor_id, f"_extract_{cat_name.replace('-', '_')}", "extractor", f"Extractor function for {cat_name}")

        for t in triggers:
            trigger_id = f"trig_{t}"
            add_node(trigger_id, t, "trigger", f"Trigger word: '{t}'")
            add_edge(trigger_id, extractor_id, "routes to")

    # 2. Process Taxonomy Keywords
    for kw, (dept, cls, fine, classpath_id) in TAXONOMY_KEYWORDS.items():
        class_id = f"class_{fine.replace(' ', '_')}"
        add_node(class_id, fine, "category", f"Taxonomy Fine Class\nDept: {dept}\nClass: {cls}")

        trigger_id = f"trig_{kw}"
        add_node(trigger_id, kw, "trigger", f"Trigger word: '{kw}'")
        add_edge(trigger_id, class_id, "classifies as")

    # 3. Process Brands & Manufacturers
    for brand, info in BRAND_VOCAB.items():
        brand_id = f"brand_{brand.replace(' ', '_')}"
        mfr = info.get("manufacturer") or "Unknown"
        alias = info.get("alias_of")
        
        details = f"OEM Brand: {brand}\nManufacturer: {mfr}"
        if alias:
            details += f"\nAlias of: {alias}"
            
        add_node(brand_id, brand, "brand", details)

        if mfr and mfr != "Unknown":
            mfr_id = f"mfr_{mfr.replace(' ', '_')}"
            add_node(mfr_id, mfr, "manufacturer", f"Manufacturer: {mfr}\nWebsite: {info.get('mfr_url', '')}")
            add_edge(brand_id, mfr_id, "made by")

    # HTML Template with Vis.js network visualization
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Elio Pipeline Relationship Mapper</title>
    <!-- Modern typography -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <!-- Vis.js CDN -->
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: 'Inter', sans-serif;
            background: #0f172a;
            color: #f1f5f9;
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        header {
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(12px);
            padding: 16px 24px;
            border-bottom: 1px solid #334155;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 10;
        }
        h1 {
            font-size: 1.25rem;
            font-weight: 700;
            background: linear-gradient(135deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .main-container {
            display: flex;
            flex: 1;
            position: relative;
            height: calc(100vh - 64px);
        }
        #network-container {
            flex: 1;
            height: 100%;
            background: #090d16;
        }
        .sidebar {
            width: 320px;
            background: rgba(15, 23, 42, 0.95);
            border-left: 1px solid #334155;
            backdrop-filter: blur(12px);
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            overflow-y: auto;
            z-index: 10;
        }
        .search-box {
            position: relative;
        }
        input {
            width: 100%;
            padding: 10px 14px;
            background: #1e293b;
            border: 1px solid #475569;
            border-radius: 8px;
            color: #f1f5f9;
            font-size: 0.9rem;
            outline: none;
            transition: border-color 0.2s;
        }
        input:focus {
            border-color: #38bdf8;
        }
        .info-panel {
            background: rgba(30, 41, 59, 0.5);
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 16px;
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .info-title {
            font-weight: 600;
            color: #38bdf8;
            font-size: 1rem;
            border-bottom: 1px solid #334155;
            padding-bottom: 8px;
        }
        .info-body {
            font-size: 0.85rem;
            line-height: 1.5;
            color: #cbd5e1;
            white-space: pre-line;
        }
        .legend {
            display: flex;
            flex-direction: column;
            gap: 8px;
            font-size: 0.8rem;
        }
        .legend-item {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .legend-color {
            width: 12px;
            height: 12px;
            border-radius: 4px;
        }
        /* Glassmorphic buttons */
        button {
            padding: 10px 16px;
            background: linear-gradient(135deg, #0284c7, #4f46e5);
            border: none;
            border-radius: 8px;
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.1s, opacity 0.2s;
        }
        button:hover {
            opacity: 0.9;
            transform: translateY(-1px);
        }
        button:active {
            transform: translateY(0);
        }
    </style>
</head>
<body>
    <header>
        <h1>Elio Relationship Mapper</h1>
        <div>
            <button onclick="resetView()">Reset View</button>
        </div>
    </header>
    <div class="main-container">
        <div id="network-container"></div>
        <div class="sidebar">
            <div class="search-box">
                <input type="text" id="node-search" placeholder="Search rules/brands/categories..." oninput="handleSearch()">
            </div>
            <div class="info-panel">
                <div class="info-title" id="detail-title">Selection Details</div>
                <div class="info-body" id="detail-body">Click on any node in the map to see its specific triggers, category classifications, or brand parent organizations.</div>
            </div>
            <div class="legend">
                <div style="font-weight: 600; margin-bottom: 4px;">Node Groups</div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #eab308;"></div>
                    <span>Trigger Keywords</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #3b82f6;"></div>
                    <span>Taxonomy Fine Classes</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #22c55e;"></div>
                    <span>OEM Brands</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #a855f7;"></div>
                    <span>Manufacturers</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #ef4444;"></div>
                    <span>Extractor Functions</span>
                </div>
            </div>
        </div>
    </div>

    <script type="text/javascript">
        // Data injected from Python
        const nodesData = %NODES_DATA%;
        const edgesData = %EDGES_DATA%;

        const container = document.getElementById('network-container');
        const data = {
            nodes: new vis.DataSet(nodesData),
            edges: new vis.DataSet(edgesData)
        };

        const options = {
            nodes: {
                font: {
                    color: '#f1f5f9',
                    size: 14,
                    face: 'Inter'
                },
                borderWidth: 2,
                shadow: true
            },
            edges: {
                color: {
                    color: '#475569',
                    highlight: '#38bdf8',
                    hover: '#64748b'
                },
                arrows: {
                    to: { enabled: true, scaleFactor: 0.8 }
                },
                width: 1,
                smooth: {
                    type: 'continuous'
                }
            },
            groups: {
                trigger: {
                    color: { background: '#eab308', border: '#ca8a04' },
                    shape: 'ellipse'
                },
                category: {
                    color: { background: '#3b82f6', border: '#2563eb' },
                    shape: 'box'
                },
                brand: {
                    color: { background: '#22c55e', border: '#16a34a' },
                    shape: 'database'
                },
                manufacturer: {
                    color: { background: '#a855f7', border: '#9333ea' },
                    shape: 'box'
                },
                extractor: {
                    color: { background: '#ef4444', border: '#dc2626' },
                    shape: 'diamond'
                }
            },
            physics: {
                solver: 'forceAtlas2Based',
                forceAtlas2Based: {
                    gravitationalConstant: -50,
                    centralGravity: 0.01,
                    springLength: 100,
                    springConstant: 0.08
                },
                stabilization: {
                    iterations: 150
                }
            },
            interaction: {
                hover: true,
                tooltipDelay: 200
            }
        };

        const network = new vis.Network(container, data, options);

        // Selection Listener
        network.on("selectNode", function (params) {
            const nodeId = params.nodes[0];
            const node = data.nodes.get(nodeId);
            
            document.getElementById('detail-title').innerText = node.label;
            document.getElementById('detail-body').innerText = node.title;

            // Highlight connections
            highlightConnections(nodeId);
        });

        network.on("deselectNode", function () {
            document.getElementById('detail-title').innerText = "Selection Details";
            document.getElementById('detail-body').innerText = "Click on any node in the map to see its specific triggers, category classifications, or brand parent organizations.";
            resetHighlights();
        });

        function highlightConnections(nodeId) {
            const connectedNodes = network.getConnectedNodes(nodeId);
            const allNodes = data.nodes.get();
            
            const updateArray = [];
            allNodes.forEach(node => {
                if (node.id === nodeId || connectedNodes.includes(node.id)) {
                    updateArray.push({ id: node.id, hidden: false, opacity: 1.0 });
                } else {
                    updateArray.push({ id: node.id, opacity: 0.15 });
                }
            });
            data.nodes.update(updateArray);
        }

        function resetHighlights() {
            const allNodes = data.nodes.get();
            const updateArray = allNodes.map(node => ({ id: node.id, opacity: 1.0 }));
            data.nodes.update(updateArray);
        }

        function handleSearch() {
            const query = document.getElementById('node-search').value.toLowerCase();
            if (!query) {
                resetHighlights();
                return;
            }

            const allNodes = data.nodes.get();
            const matchedNode = allNodes.find(n => n.label.toLowerCase().includes(query));
            
            if (matchedNode) {
                network.selectNodes([matchedNode.id]);
                highlightConnections(matchedNode.id);
                network.focus(matchedNode.id, {
                    scale: 1.0,
                    animation: { duration: 500 }
                });
                document.getElementById('detail-title').innerText = matchedNode.label;
                document.getElementById('detail-body').innerText = matchedNode.title;
            }
        }

        function resetView() {
            document.getElementById('node-search').value = "";
            resetHighlights();
            network.fit({
                animation: { duration: 1000 }
            });
        }
    </script>
</body>
</html>
"""

    # Inject data into HTML template
    html_content = html_template.replace("%NODES_DATA%", json.dumps(nodes, indent=4))
    html_content = html_content.replace("%EDGES_DATA%", json.dumps(edges, indent=4))

    # Write output file
    output_path = ROOT / "rules_map.html"
    output_path.write_text(html_content, encoding="utf-8")
    print(f"Wrote rules_map.html successfully at {output_path}")


if __name__ == "__main__":
    main()
