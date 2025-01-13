from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, DataPoint

def create_app(config=None):
    app = Flask(__name__)
    if config:
        app.config.update(config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_points.db'

    db.init_app(app)

    @app.before_request
    def create_tables():
        db.create_all()

    @app.route('/')
    def home():
        data_points = db.session.scalars(db.select(DataPoint)).all()
        return render_template('home.html', data_points=data_points)

    @app.route('/add', methods=['GET', 'POST'])
    def add():
        if request.method == 'POST':
            try:
                feature1 = float(request.form['feature1'])
                feature2 = float(request.form['feature2'])
                category = int(request.form['category'])
                db.session.add(DataPoint(feature1=feature1, feature2=feature2, category=category))
                db.session.commit()
                return redirect(url_for('home'))
            except ValueError:
                return render_template("error.html", error_code='400 Bad Request',
                                       error_message='Invalid input data.'), 400
        else:
            return render_template('add.html')

    @app.route('/delete/<int:record_id>', methods=['POST'])
    def delete_data_point(record_id):
        data_point = db.session.scalars(db.select(DataPoint).where(DataPoint.id == record_id)).first()
        if data_point:
            db.session.delete(data_point)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            return render_template("error.html", error_code='404 Not Found',
                                   error_message='Record not found.'), 404

    @app.route('/api/data', methods=['GET'])
    def api_get_data():
        data_points = db.session.scalars(db.select(DataPoint)).all()
        return jsonify([{
            "id": dp.id,
            "feature1": dp.feature1,
            "feature2": dp.feature2,
            "category": dp.category
        } for dp in data_points])

    @app.route('/api/data', methods=['POST'])
    def api_add_data():
        data = request.get_json()
        try:
            feature1 = float(data['feature1'])
            feature2 = float(data['feature2'])
            category = int(data['category'])
            new_data_point = DataPoint(feature1=feature1, feature2=feature2, category=category)
            db.session.add(new_data_point)
            db.session.commit()
            return jsonify({"id": new_data_point.id}), 201
        except (ValueError, KeyError):
            return jsonify({"error": "Invalid data"}), 400

    @app.route('/api/data/<int:record_id>', methods=['DELETE'])
    def api_delete_data(record_id):
        data_point = db.session.scalars(db.select(DataPoint).where(DataPoint.id == record_id)).first()
        if data_point:
            db.session.delete(data_point)
            db.session.commit()
            return jsonify({"id": record_id}), 200
        else:
            return jsonify({"error": "Record not found"}), 404

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()