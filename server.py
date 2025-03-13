import os
from flask import Flask, request, render_template_string
import openai
from dotenv import load_dotenv

load_dotenv()  # Load the environment variables from the .env file

app = Flask(__name__)

client = openai.OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"), base_url=os.environ.get("LLM_ENDPOINT")
)

HTML_TEMPLATE = """
<!DOCTYPE html> 
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI-Generated Email</title>
<style>
body {
font-family: Arial, sans-serif;
margin:20px;
padding:20px;
background-color: #f8f9fa;
}

.container {
max-width: 600px;
margin:auto;
padding:20px;
background-color: #ffffff;
border: 1px solid #ddd;
border-radius: 5px;
box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

h1 {
color : #333;
}

form {
margin-bottom: 20px;
}


textarea {
width: 100%;
height: 100px;
margin-bottom: 10px;
padding: 10px;
border: 1px solid #ddd;
border-radius: 5px;
}

button {
padding : 10px 20px;
background-color: #007bff;
color: white;
border: none;
border-radius: 5px;
cursor: pointer;
}

button:hover {
background-color: #0056b3;
} 

pre {
background-color: #f4f4f4;
padding:10px;
border-radius: 5px;
overflow-x:auto;
}

</style>
</head>
<body>
<div class="container">
<h1>AI Email Generator</h1>
<form method="POST"> 
<textarea name="input" placeholder="Enter your prompt here..."></textarea>
<button type="submit">Generate Email</button>
</form>
{% if email %}
<h2>Your AI-Generated Email</h2>
<pre>{{ email }}</pre>
{% endif %}
</div> 
</body>
</html>

"""


@app.route("/", methods=["GET", "POST"])
def index():
    email = None
    if request.method == "POST":
        try:
            input_message = request.form["input"]
            response = client.chat.completions.create(
                model=os.environ.get("MODEL_NAME"),
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI chatbot which specializes in writing emails.",
                    },
                    {"role": "user", "content": input_message},
                ],
            )
            print(response)
            email = response.choices[0].message.content
        except Exception as e:
            print("Error: ", str(e))
            email = "An error occurred when trying to generate the email."
    return render_template_string(HTML_TEMPLATE, email=email)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
