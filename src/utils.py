"""
Utility functions for the fish recognition system.
Only used in the UI layer.
"""

conservation_status_mapping = {
    "LC": {
        "label": "Least Concern",
        "color": "#059669",  # green
    },
    "NT": {
        "label": "Near Threatened",
        "color": "#eab308",  # amber
    },
    "VU": {
        "label": "Vulnerable",
        "color": "#f97316",  # orange
    },
    "EN": {
        "label": "Endangered",
        "color": "#ea580c",  # deep orange
    },
    "CR": {
        "label": "Critically Endangered",
        "color": "#dc2626",  # red
    },
    "DD": {
        "label": "Data Deficient",
        "color": "#6b7280",  # gray
    },
    "N/A": {
        "label": "Not Available",
        "color": "#6b7280",  # gray
    },
}

def map_conservation_status(status_code: str) -> dict:
    """
    Map a conservation status code (e.g., LC, VU, CR) to full label and color.
    
    Returns a dict with:
        - code: original code
        - label: human-readable label
        - color: hex color for UI
    """
    if not status_code:
        status_code = "N/A"

    code = status_code.strip().upper()

    

    base = conservation_status_mapping.get(
        code,
        conservation_status_mapping["N/A"],
    )
    
    return {
        "code": code,
        **base,
    }


def get_conservation_status(status_code: str = None):
    """
    Get conservation status data for Gradio HighlightedText component.
    
    Args:
        status_code: If provided, returns HighlightedText format for that code.
                    If None, returns color map for all status codes.
    
    Returns:
        - If status_code provided: list of tuples (text, category) for HighlightedText
        - If status_code is None: dict mapping status codes to hex colors
    """
    if status_code is not None:
        # Return HighlightedText format for specific status code
        info = map_conservation_status(status_code)
        status_text = f"{info['code']} · {info['label']}"
        return [(status_text, info['code'])]
    else:
        # Return color map for all status codes
        color_map = {}
        status_codes = conservation_status_mapping.keys()
        for code in status_codes:
            info = map_conservation_status(code)
            color_map[code] = info['color']
        return color_map