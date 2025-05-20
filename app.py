from flask import Flask, request, render_template_string
import random
import string
import os


app = Flask(__name__)

def evaluate_password(password):
    length = len(password)
    has_letters = any(c.isalpha() for c in password)
    has_digits = any(c.isdigit() for c in password)
    has_symbols = any(c in string.punctuation for c in password)

    if length >= 12 and has_letters and has_digits and has_symbols:
        return "Strong", "green"
    elif length >= 8 and ((has_letters and has_digits) or (has_letters and has_symbols) or (has_digits and has_symbols)):
        return "Medium", "orange"
    else:
        return "Weak", "red"

def generate_password(length, seed_value, include_letters, include_digits, include_symbols):
    caracteres = ""
    if include_letters:
        caracteres += string.ascii_letters
    if include_digits:
        caracteres += string.digits
    if include_symbols:
        caracteres += string.punctuation

    if not caracteres:
        return "Erreur: Veuillez sélectionner au moins un type de caractère.", "red"

    if seed_value:
        random.seed(seed_value)

    mot_de_passe = ''.join(random.choice(caracteres) for _ in range(length))
    level, color = evaluate_password(mot_de_passe)
    return mot_de_passe, level, color

html = """
<!doctype html>
<html lang="fr">
  <head>
    <meta charset="utf-8">
    <title>Password generator</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 20px; }
      .container { max-width: 600px; margin: auto; }
      .result { margin-top: 20px; }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>🔐 Password generator</h1>
      <form method="post">
        <label for="length">Password length :</label>
        <input type="number" id="length" name="length" value="12" required><br><br>
        
        <label for="seed">Seed (optional) :</label>
        <input type="text" id="seed" name="seed"><br><br>
        
        <input type="checkbox" id="letters" name="letters" checked>
        <label for="letters">Include letters</label><br>
        
        <input type="checkbox" id="digits" name="digits" checked>
        <label for="digits">Include numbers</label><br>
        
        <input type="checkbox" id="symbols" name="symbols">
        <label for="symbols">Include symbols</label><br><br>
        
        <button type="submit">Generate</button>
      </form>
      
      {% if password %}
      <div class="result">
        <h2>Password generated :</h2>
        <input type="text" value="{{ password }}" readonly style="width: 100%;"><br><br>
        <p style="color: {{ color }}">🔒 Password level : {{ level }}</p>
      </div>
      {% endif %}
    </div>
  </body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    password = None
    level = None
    color = None
    if request.method == 'POST':
        length = int(request.form['length'])
        seed = request.form['seed']
        include_letters = 'letters' in request.form
        include_digits = 'digits' in request.form
        include_symbols = 'symbols' in request.form
        password, level, color = generate_password(length, seed, include_letters, include_digits, include_symbols)
    return render_template_string(html, password=password, level=level, color=color)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

