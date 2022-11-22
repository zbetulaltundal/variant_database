from flask import Flask
from views import *
from common_funcs import *

app = Flask(__name__)

if __name__ == "__main__":
    
    app.config.from_pyfile("config.py")
    # home page
    app.add_url_rule("/", view_func=home_page, methods=['GET'])
    app.add_url_rule("/terimler", view_func=dict_page, methods=['GET'])
    app.add_url_rule("/", view_func=upload_vcf_file, methods=["GET", "POST"])
    app.add_url_rule('/varyant-bilgisi', view_func=variant_info, methods=['GET' , "POST"])

    app.run(host="0.0.0.0", port=8080)

 