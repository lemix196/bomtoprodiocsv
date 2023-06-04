from flask import Flask, render_template, request, send_from_directory, send_file, flash
import prodiocsv as pcsv
import pandas as pd
from form_validators import FormValidator

app = Flask(__name__)
app.secret_key = 'kkeeyy'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files["file"]
        prepare_date = request.form["prepare-date"]
        finish_date = request.form["finish-date"]
        is_urgent = bool(request.form.getlist("isUrgent"))

        fv = FormValidator(file, file.filename, prepare_date, finish_date, is_urgent)

        # form validation
        if fv.validate_form() != None:
            return fv.validate_form()
            
        ### CSV CREATION
    # init of empty DataFrame object to be filled with lines to export to Prodio
        machining_df = pd.DataFrame(columns=pcsv.PRODIO_IMPORT_HEADERS)
        prepare_materials_df = pd.DataFrame(columns=pcsv.PRODIO_IMPORT_HEADERS)
        client_name = pcsv.get_client_name(file.filename)
        bom_data = pcsv.convert_xls_to_dataframe(file)

        # iteration through whole bom_csv file/DataFrame to pick data from it and swap to prodio csv
        for i in range(len(bom_data)):
            # read single line with i index
            line = bom_data.loc[i]
            p = pcsv.Product()
            p.get_product_data(line)
            pcsv.write_validated_line(product=p,
                                validators=pcsv.validate_bom_line(p),
                                prepare_dataframe=prepare_materials_df,
                                machine_dataframe=machining_df,
                                client_name=client_name,
                                ext_order_number="nr_zamowienia",
                                prepare_finish_date=prepare_date,
                                finish_date=finish_date,
                                is_urgent=is_urgent
                                )

        merged_df = pd.concat([machining_df, prepare_materials_df], ignore_index=True, sort=False)
        csv_filename = 'generated_prodio_import.csv'
        merged_df.to_csv(csv_filename, sep=";", index=False)
        ### END OF CSV CREATION
        flash('Plik CSV zostal wygenerowany', 'Success')
        return send_file(csv_filename, as_attachment=True)
    
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)