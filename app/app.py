from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Girly App ✨</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@700&family=Quicksand:wght@500;700&display=swap" rel="stylesheet">
    <style>
        body {
            background-color: #F3E8FF;
            color: #3B0764;
            font-family: 'Quicksand', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            overflow: hidden;
            position: relative;
        }
        .container {
            text-align: center;
            background: white;
            padding: 2.5rem;
            border-radius: 24px;
            box-shadow: 0 10px 25px rgba(124, 58, 237, 0.1);
            border: 2px solid #F472B6;
            z-index: 10;
        }
        h1 {
            color: #7C3AED;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        p {
            font-size: 1.1rem;
            color: #3B0764;
        }
        .badges {
            margin: 1.5rem 0;
        }
        .badge {
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 50px;
            font-size: 0.85rem;
            font-weight: bold;
            margin: 0 0.25rem;
        }
        .badge-version { background-color: #7C3AED; color: white; }
        .badge-cluster { background-color: #F472B6; color: white; }
        .signature {
            font-family: 'Caveat', cursive;
            font-size: 2.2rem;
            color: #F472B6;
            margin-top: 1.5rem;
        }
        /* Paillettes en arrière-plan */
        .sparkle {
            position: absolute;
            background: #F472B6;
            border-radius: 50%;
            opacity: 0.5;
            animation: float 6s infinite ease-in-out;
        }
        @keyframes float {
            0%, 100% { transform: translateY(0) scale(1); }
            50% { transform: translateY(-20px) scale(1.2); }
        }
    </style>
</head>
<body>
    <div class="sparkle" style="top: 15%; left: 15%; width: 12px; height: 12px; animation-delay: 0s;"></div>
    <div class="sparkle" style="top: 25%; left: 85%; width: 8px; height: 8px; animation-delay: 1.5s;"></div>
    <div class="sparkle" style="top: 75%; left: 20%; width: 14px; height: 14px; animation-delay: 3s;"></div>
    <div class="sparkle" style="top: 80%; left: 80%; width: 10px; height: 10px; animation-delay: 4.5s;"></div>

    <div class="container">
        <h1>Application Mauve ✨</h1>
        <p>Bienvenue sur votre magnifique application personnalisée !</p>
        <div class="badges">
            <span class="badge badge-version">Version: 1.0.0</span>
            <span class="badge badge-cluster">Cluster: Active</span>
        </div>
        <div class="signature">Aicha</div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api')
def api():
    return jsonify({"status": "success", "message": "Welcome to the API"})

@app.route('/healthz')
def healthz():
    return jsonify({"status": "healthy"}), 200

@app.route('/readyz')
def readyz():
    return jsonify({"status": "ready"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)