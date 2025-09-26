import os
from flask import Flask, request, jsonify, render_template
from src.ai_news_agents.crew import AiNewsAgents
import markdown2
from datetime import datetime

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/run', methods=['POST'])
def run_crew():
    data = request.json
    topic = data.get('topic')

    if not topic:
        return jsonify({'error': 'Topic is required'}), 400

    # Ensure the 'news' directory exists
    if not os.path.exists('news'):
        os.makedirs('news')

    inputs = {
        'topic': topic,
        'date': datetime.now().strftime('%Y-%m-%d')
    }

    try:
        crew_instance = AiNewsAgents()
        result = crew_instance.crew().kickoff(inputs=inputs)

        # Define the expected output file path based on the crew's logic
        output_filename = f"news/comprehensive_ai_news_report.md"

        if os.path.exists(output_filename):
            with open(output_filename, 'r') as f:
                report_md = f.read()
            report_html = markdown2.markdown(report_md)
            return jsonify({'report': report_html})
        else:
            return jsonify({'error': 'Report file not found.'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)