import os, csv
from models import Data
from datetime import datetime
from utils.visualize import visualize
from forms import DataForm, UploadForm
from werkzeug.utils import secure_filename
from flask_paginate import Pagination, get_page_args
from utils.functions import predict, analyze_market
from user.common import get_logged_in_user, get_trained_model,get_and_load_user_data
from flask import Blueprint, request, render_template, jsonify, flash, redirect, url_for


def user_blueprint(app, db_session):

    user_bp = Blueprint('user', __name__)

    @user_bp.route('/user/markets', methods=['GET'])
    def get_markets():
        user = get_logged_in_user(db_session)
        data = db_session.query(Data).filter_by(user_id=user.id).all()
        if data is None:
            return jsonify({'error': 'Data loading failed'})
        else:
            # Extract unique and non-null 'market' values using list comprehension
            markets = {entry.market for entry in data if entry.market}
            # Convert set to list and return as JSON
            return jsonify({'markets': list(markets)})


    # API route to fetch list of categories
    @user_bp.route('/user/categories', methods=['GET'])
    def get_categories():
        user = get_logged_in_user(db_session)
        data = db_session.query(Data).filter_by(user_id=user.id).all()
        if data is None:
            return jsonify({'error': 'Data loading failed'})
        else:
            # Extract unique and non-null 'market' values using list comprehension
            categories = {entry.category for entry in data if entry.category}
            # Convert set to list and return as JSON
            return jsonify({'categories': list(categories)})
    
    # Get User Data Currency
    @user_bp.route('/user/data/currency', methods=['GET'])
    def get_currency():
        user = get_logged_in_user(db_session)
        data = db_session.query(Data).filter_by(user_id=user.id).first()
        if data is not None:
            return jsonify({'currency': data.currency})
        else:
            return jsonify({'error': 'Data retrieving currency'})

    @user_bp.route('/user/data', methods=['GET'])
    # @login_required
    def data():
        # user = current_user
        user = get_logged_in_user(db_session)
        # Get page arguments for pagination
        page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
        # Query the database for the current user's data
        data =  db_session.query(Data).filter_by(user_id=user.id)
        user_data = data.order_by(Data.date.desc()).offset(offset).limit(per_page).all()
        # Create a Pagination object
        pagination = Pagination(page=page, per_page=20, total=data.count(), css_framework='bootstrap4')

        return render_template('user_data.html', user_data=user_data, page=page, per_page=per_page, pagination=pagination)

    #Upload User Data
    @user_bp.route('/user/data/upload', methods=['GET','POST'])
    def upload_csv():
        form = UploadForm()
        if form.validate_on_submit():
            file = form.data.data  # Get the FileStorage object from the form
            if file:
                # user = current_user
                user = get_logged_in_user(db_session)
                filename = secure_filename(file.filename)  # Secure the filename
                file.save(os.path.join(app.config['upload_path'], filename))  # Save the file
                with open(os.path.join(app.config['upload_path'], filename), 'r') as f:
                    reader = csv.reader(f)
                    next(reader)  # Skip the header row
                    for row in reader:
                        new_data = Data(
                            date=datetime.strptime(row[0], '%Y-%m-%d'),
                            market=row[1],
                            category=row[2],
                            commodity=row[3],
                            unit=row[4],
                            currency=row[5],
                            price=float(row[6]),
                            user_id=user.id
                        )
                        db_session.add(new_data)
                    db_session.commit()
                flash('Data uploaded successfully!', 'success')
                return redirect(url_for('user.data'))
            else:
                flash('No file selected!', 'error')
        return render_template('upload_csv.html', form=form)


    # Route for User input
    @user_bp.route('/user/data/input', methods=['GET','POST'])
    # @login_required
    def add_data():
        form = DataForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                # user = current_user
                user = get_logged_in_user(db_session)
                new_data = Data(
                    date=datetime.strptime(form.date.data, '%Y-%m-%d'),
                    market=form.market.data,
                    category=form.category.data,
                    commodity=form.commodity.data,
                    unit=form.unit.data,
                    currency=form.currency.data,
                    price=float(form.price.data),
                    user_id=user.id
                )
                db_session.add(new_data)
                db_session.commit()
                flash('Data inputted successfully!', 'success')
                return redirect(url_for('user.data'))
            else:
                flash('Error: Invalid input.', 'error')
        return render_template('add_data.html', form=form)

    # User data prediction route
    @user_bp.route('/user/data/prediction', methods=['GET','POST'])
    # @login_required
    def user_data_prediction():
        if request.method == 'POST':
            # Get the input data from the request
            input_data = request.get_json()
            # Check if the required fields are in the input data
            if 'category' not in input_data and 'market' not in input_data:
                return jsonify({'error': 'Either category or market is required.'})
                # Get the category and market from the input data

            data = get_and_load_user_data(db_session)
            if data is None:
                return jsonify({'error': 'Either category or market is required.'})
            model, enc = get_trained_model(data)
            market = input_data.get('market')
            category = input_data.get('category')
            prediction = predict(model, enc, category, market)
            return jsonify({'prediction': prediction.tolist()})
        else:
            return render_template('user_prediction.html')

    #User data visualization route
    @user_bp.route('/user/data/visualization', methods=['GET'])
    # @login_required
    def user_data_visualization():
        data = get_and_load_user_data(db_session)
        # Check if data is loaded and processed successfully
        if data is None:
            flash('Error: Failed to load and process user data.', 'error')  # 
            return render_template('user_visualization.html')
        else:
            visualize(data)
            return render_template('user_visualization.html')    

    # User Market analysis route
    @user_bp.route('/user/data/analysis', methods=['GET', 'POST'])
    # @login_required
    def user_data_analysis():
        if request.method == "POST":
            data = get_and_load_user_data(db_session)
            if data is not None:
                return analyze_market(data)
            return jsonify({'error': 'Failed to load and process user data'})
        return render_template('user_analysis.html')

    return user_bp