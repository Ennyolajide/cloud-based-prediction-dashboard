from utils.visualize import visualize
from utils.functions import predict, analyze_market, simulate_market
from flask import Blueprint, request, render_template, jsonify, flash


def loaded_blueprint(data,model, enc):

    loaded_bp = Blueprint('loaded', __name__)

    @loaded_bp.route('/markets', methods=['GET'])
    def get_markets():
        if data is None:
            return jsonify({'error': 'Data loading failed'})
        else:
            markets = data['market'].unique().tolist()
            return jsonify({'markets': markets})

    # API route to fetch list of categories
    @loaded_bp.route('/categories', methods=['GET'])
    def get_categories():
        if data is None:
            return jsonify({'error': 'Data loading failed'})
        else:
            categories = data['category'].unique().tolist()
            return jsonify({'categories': categories})
        
       # Get User Data Currency
    @loaded_bp.route('/currency', methods=['GET'])
    def get_currency():
        if data is not None:
            print('Currency:', '')
            return jsonify({'currency': 'NGN'})
        else:
            return jsonify({'error': 'Data retrieving currency'})


    @loaded_bp.route('/prediction', methods=['GET','POST'])
    # @login_required
    def prediction():
        if request.method == "POST":
        # Get the input data from the request
            input_data = request.get_json()
            # Check if the required fields are in the input data
            if 'category' not in input_data and 'market' not in input_data:
                return jsonify({'error': 'Either category or market is required.'}), 400

            if data is None:
                return jsonify({'error': 'Either category or market is required.'})
            market = input_data.get('market')
            category = input_data.get('category')
            prediction = predict(model, enc, category, market)
            return jsonify({'prediction': prediction.tolist()})
        else:
            return render_template('prediction.html')


    # Visualization route
    @loaded_bp.route('/visualization', methods=['GET'])
    # @login_required
    def visualization():
        if data is None:
            flash('Error: Failed to load and process user data.', 'error')  # 
            return render_template('visualization.html')
        else:
            visualize(data)
            return render_template('visualization.html')

    # Market analysis route
    @loaded_bp.route('/analysis', methods=['GET', 'POST'])
    # @login_required
    def analysis():
        if request.method == "POST":
            if data is not None:
                return analyze_market(data)
            return jsonify({'error': 'Failed to load and process user data'})
        return render_template('analysis.html')


    # Simulation view route
    @loaded_bp.route('/simulation/view', methods=['GET'])
    # @login_required
    def show_simulation():
        return render_template('simulation.html')

    # Simulation route
    @loaded_bp.route('/simulation', methods=['GET'])
    # @login_required
    def simulation():
        num_markets = request.args.get('num_markets', type=int)
        num_commodities = request.args.get('num_commodities', type=int)
        
        if num_markets is None or num_commodities is None:
            return jsonify({'error': 'Both num_markets and num_commodities are required.'}), 400
        
        if num_markets <= 0 or num_commodities <= 0:
            return jsonify({'error': 'Both num_markets and num_commodities must be greater than zero.'}), 400
        
        if data is None:
            return jsonify({'error': 'Data loading failed'}), 500

        return jsonify({'simulation': simulate_market(data, num_markets, num_commodities)})


    return loaded_bp