from flask import Flask, request, render_template
import pickle
import pandas as pd

#Loading the model and the scaler
model = pickle.load(open('xgb_model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))


app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def prediction():
    if request.method == 'POST':
        Age = int(request.form['age'])
        Gender = request.form['gender']
        BMI = float(request.form['bmi'])
        Children = request.form['children']
        Smoker = request.form['smoker']
        Region = request.form['region']

        x_query = [[Age, Gender, BMI, Children, Smoker, Region]] 
        features = ['age', 'sex', 'bmi', 'children', 'smoker', 'region']
        df = pd.DataFrame(x_query, columns=features)
        print(df)


        #Adding the OHE features
        if Gender == 'male':
            df['sex_male'] = 1
        else:
            df['sex_male'] = 0

        if Smoker == 'yes':
            df['smoker_yes'] = 1
        else:
            df['smoker_yes'] = 0

        if Region == 'northwest':
            df['region_northwest'] = 1
            df['region_southeast'] = 0
            df['region_southwest'] = 0
        elif Region == 'southeast':
            df['region_northwest'] = 0
            df['region_southeast'] = 1
            df['region_southwest'] = 0
        elif Region == 'southwest':
            df['region_northwest'] = 0
            df['region_southeast'] = 0
            df['region_southwest'] = 1
        else:
            df['region_northwest'] = 0
            df['region_southeast'] = 0
            df['region_southwest'] = 0


        #extra_features = ['sex_male', 'smoker_yes', 'region_northwest', 'region_southeast', 'region_southwest']

        df_prepared = df.drop(labels=[ 'sex', 'smoker', 'region'], axis = 1)
        print("DF Prepared: \n",df_prepared)
        x_test = scaler.transform(df_prepared)
        print("x_test\n", x_test)
        y_pred = model.predict(x_test)
        print("Query point : ", x_query)
        print("Cost will be around Rs. ", y_pred)

        return render_template('result.html', cost = y_pred[0])


        #return render_template('result.html', age = Age, gender = Gender, bmi = BMI, children = Children, smoker = Smoker, region = Region)
    return render_template('home.html')



if __name__ == '__main__':
    app.run(debug = True)

