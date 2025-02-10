import gradio as gr
import requests

def get_microposts():
    """
    Retrieve actual microposts from a real REST API endpoint.
    """
    try:
        # Call an external REST API endpoint.
        response = requests.get("http://localhost:3000/api/v1/microposts")
        response.raise_for_status()
        posts = response.json()
        # Format the microposts for display.
        output_str = "\n".join([f"ID: {post['id']} - Title: {post['title']}" for post in posts])
        return output_str
    except requests.RequestException as e:
        return f"Error: {e}"

with gr.Blocks() as demo:
    gr.Markdown("## GET /api/v1/microposts")
    output_text = gr.Textbox(label="Microposts", lines=5)
    get_button = gr.Button("Get Microposts")
    get_button.click(fn=get_microposts, inputs=[], outputs=output_text)

if __name__ == "__main__":
    demo.launch()