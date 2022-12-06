from flask import Flask
from views import *
app = Flask(__name__)

if __name__ == "__main__":
    
    app.config.from_pyfile("config.py")
    # home page
    app.add_url_rule("/", view_func=home_page, methods=['GET'])
    app.add_url_rule("/anasayfa", view_func=home_page, methods=['GET'])
    
    app.add_url_rule("/", view_func=upload_vcf_file, methods=['GET',"POST"])
    app.add_url_rule("/anasayfa", view_func=upload_vcf_file, methods=["GET", "POST"])


    app.add_url_rule("/veri-ekle", view_func=add_data_page, methods=["GET"])
    app.add_url_rule("/veri-ekle", view_func=add_data, methods=["GET", "POST"])

    app.add_url_rule("/terimler", view_func=dict_page, methods=['GET'])
    app.add_url_rule('/tarama-sonuclari', view_func=list_results, methods=['GET' , 'POST'])
    app.add_url_rule("/tarama-sonuclari?chrom=<chrom>&pos=<pos>&alt=<alt>&ref=<ref>", view_func=variant_details)

    app.run(debug=True, host="0.0.0.0", port=8080)

 