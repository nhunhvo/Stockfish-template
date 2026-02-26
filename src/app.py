"""
UI to prototype the fish recognition system with Gradio.
"""

import gradio as gr
import os

# Get static directory path
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")

# Get example images from static directory
def get_example_images():
    """Get list of example image paths from static directory."""
    example_images = []
    if os.path.exists(static_dir):
        image_extensions = ['.jpeg', '.jpg', '.png']
        for filename in sorted(os.listdir(static_dir)):
            if any(filename.lower().endswith(ext) for ext in image_extensions):
                example_images.append(os.path.join(static_dir, filename))
    return example_images[:10]


def recognize_fish(image):
    """
    Recognize fish based on uploaded image.
    
    Returns:
        tuple: (markdown_output, highlighted_status) for the UI components
    """
    if image is None:
        return "Please upload an image to recognize fish.", None
    # Save temporary image if needed
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
        image.save(tmp_file.name)
        tmp_path = tmp_file.name

    # Format markdown output (without conservation status, as it's shown separately)
    output = """# Top Match in FishVectorDB:

Pelican
"""
    return output

# Create Gradio interface
def create_ui():
    """Create and launch the Gradio interface."""
    example_images = get_example_images()
    
    with gr.Blocks(title="Stockfish AI") as demo:
        gr.Markdown("# 🐟 Stockfish AI")
        gr.Markdown("Upload an image or select an example to identify most similar fish species.")
        
        with gr.Row():
            with gr.Column():
                image_input = gr.Image(
                    type="pil",
                    label="Upload Fish Image",
                    height=400
                )

                # Add example images
                if example_images:
                    gr.Examples(
                        examples=example_images,
                        inputs=image_input,
                        label="Example Images"
                    )
            with gr.Column():
                output = gr.Markdown(label="Search Results")

        image_input.change(
            fn=recognize_fish,
            inputs=image_input,
            outputs=[output]
        )
    return demo


if __name__ == "__main__":
    demo = create_ui()
    demo.launch(share=False)