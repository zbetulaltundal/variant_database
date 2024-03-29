from flask import Flask

from views import *

import jinja2

app = Flask(__name__)

env = jinja2.Environment()
env.globals.update(zip=zip)

if __name__ == "__main__":
    
    app.config.from_pyfile("config.py")
    # home page
    app.add_url_rule("/", view_func=home_page, methods=['GET'])
    app.add_url_rule("/anasayfa", view_func=home_page, methods=['GET'])
    
    app.add_url_rule("/tarama-sonuclari", view_func=upload_vcf_file, methods=["GET", "POST"])
    app.add_url_rule("/tarama-sonuclari?chrom=<chrom>&pos=<pos>&alt=<alt>&ref=<ref>&hgnc=<hgnc>", view_func=variant_details, methods=["GET"])
    app.add_url_rule("/sonuc-indir", view_func=download_data, methods=["GET", "POST"])

    app.add_url_rule("/veri-ekle", view_func=add_data_page, methods=["GET"])
    app.add_url_rule("/veri-ekle", view_func=add_data, methods=["GET", "POST"])
    app.add_url_rule("/terimler", view_func=dict_page, methods=['GET'])
    app.add_url_rule("/kullanici-veritabani", view_func=userdb_variants, methods=['GET'])
    app.add_url_rule("/kullanici-veritabani?chrom=<chrom>&pos=<pos>&alt=<alt>&ref=<ref>", view_func=user_variant_details, methods=["GET"])

    app.run(debug=True, host="0.0.0.0", port=8080)
