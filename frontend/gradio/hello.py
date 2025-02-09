import gradio as gr

def say_hello():
    # Return a simple Hello World message.
    return "Hello, World!"

# Create a Gradio interface with no input component and a text output.
iface = gr.Interface(
    fn=say_hello,
    inputs=[], 
    outputs="text", 
    title="Hello World Interface",
    description="A simple Gradio Hello World example."
)

if __name__ == "__main__":
    # Launch the Gradio interface.
    iface.launch()