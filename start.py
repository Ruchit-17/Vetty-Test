import chardet
from flask import Flask, request, jsonify

app = Flask(__name__)

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        rawdata = file.read()
        result = chardet.detect(rawdata)
        
    if result['encoding'] is None:
        return 'utf-8'
    return result['encoding']

@app.route("/fetchdetails",methods=['GET'])
def fetchdetails():
    try:
        # Optional params       
        file_name = str(request.args.get('file_name', "file1.txt"))
        line_start = int(request.args.get('line_start', 0))
        line_end = int(request.args.get('line_end', -1))
        
        file_path = f'./files/{file_name}'
        encoding = detect_encoding(file_path)
        with open(file_path, 'r',encoding=encoding) as file:
            lines = file.readlines()[line_start:line_end] if line_end != -1 else file.readlines()[line_start:]

        html_content = '<html><body>'
        for line in lines:
            html_content += f'<p>{line}</p>'
        html_content += '</body></html>'
        return html_content
    
    except Exception as e:
        html_content = '<html><body>'
        html_content += '<p>Error Description :: </p>'
        html_content += f'<p>{str(e)}</p>'
        return html_content
    
    

if __name__ == '__main__':
    app.run()
