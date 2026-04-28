import matplotlib.pyplot as plt
import joblib

def export_feature_importance():
    model = joblib.load('climateguard_v1_model.pkl')
    features = ['Rainfall', 'Temp', 'Humidity', 'Water Index']
    importances = model.feature_importances_
    
    plt.barh(features, importances)
    plt.title('ClimateGuard: Key Drivers of Health Risk')
    plt.savefig('../docs/visuals/feature_importance.png')
