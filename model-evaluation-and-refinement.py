#!/usr/bin/env python
# coding: utf-8

# <div class="alert alert-block alert-info" style="margin-top: 20px">
#     <a href="http://cocl.us/DA0101EN_NotbookLink_Top">
#          <img src="https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DA0101EN/Images/TopAd.png" width="750" align="center">
#     </a>
# </div>

# <a href="https://www.bigdatauniversity.com"><img src="https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DA0101EN/Images/CCLog.png" width=300, align="center"></a>
# 
# <h1 align=center><font size=5>Data Analysis with Python</font></h1>

# <h1>Module 5: Model Evaluation and Refinement</h1>
# 
# We have built models and made predictions of vehicle prices. Now we will determine how accurate these predictions are. 

# <h1>Table of content</h1>
# <ul>
#     <li><a href="#ref1">Model Evaluation </a></li>
#     <li><a href="#ref2">Over-fitting, Under-fitting and Model Selection </a></li>
#     <li><a href="#ref3">Ridge Regression </a></li>
#     <li><a href="#ref4">Grid Search</a></li>
# </ul>

# In[1]:


import pandas as pd
import numpy as np

# Import clean data 
path = 'https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DA0101EN/module_5_auto.csv'
df = pd.read_csv(path)


# In[3]:


df.to_csv('module_5_auto.csv')


#  First lets only use numeric data 

# In[4]:


df=df._get_numeric_data()
df.head()


#  Libraries for plotting 

# In[5]:


get_ipython().run_cell_magic('capture', '', '! pip install ipywidgets')


# In[6]:


from IPython.display import display
from IPython.html import widgets 
from IPython.display import display
from ipywidgets import interact, interactive, fixed, interact_manual


# <h2>Functions for plotting</h2>

# In[7]:


def DistributionPlot(RedFunction, BlueFunction, RedName, BlueName, Title):
    width = 12
    height = 10
    plt.figure(figsize=(width, height))

    ax1 = sns.distplot(RedFunction, hist=False, color="r", label=RedName)
    ax2 = sns.distplot(BlueFunction, hist=False, color="b", label=BlueName, ax=ax1)

    plt.title(Title)
    plt.xlabel('Price (in dollars)')
    plt.ylabel('Proportion of Cars')

    plt.show()
    plt.close()


# In[8]:


def PollyPlot(xtrain, xtest, y_train, y_test, lr,poly_transform):
    width = 12
    height = 10
    plt.figure(figsize=(width, height))
    
    
    #training data 
    #testing data 
    # lr:  linear regression object 
    #poly_transform:  polynomial transformation object 
 
    xmax=max([xtrain.values.max(), xtest.values.max()])

    xmin=min([xtrain.values.min(), xtest.values.min()])

    x=np.arange(xmin, xmax, 0.1)


    plt.plot(xtrain, y_train, 'ro', label='Training Data')
    plt.plot(xtest, y_test, 'go', label='Test Data')
    plt.plot(x, lr.predict(poly_transform.fit_transform(x.reshape(-1, 1))), label='Predicted Function')
    plt.ylim([-10000, 60000])
    plt.ylabel('Price')
    plt.legend()


# <h1 id="ref1">Part 1: Training and Testing</h1>
# 
# <p>An important step in testing your model is to split your data into training and testing data. We will place the target data <b>price</b> in a separate dataframe <b>y</b>:</p>

# In[9]:


y_data = df['price']


# drop price data in x data

# In[10]:


x_data=df.drop('price',axis=1)


# Now we randomly split our data into training and testing data  using the function <b>train_test_split</b>. 

# In[65]:


from sklearn.model_selection import train_test_split


x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.15, random_state=1)


print("number of test samples :", x_test.shape[0])
print("number of training samples:",x_train.shape[0])


# The <b>test_size</b> parameter sets the proportion of data that is split into the testing set. In the above, the testing set is set to 10% of the total dataset. 

# <div class="alert alert-danger alertdanger" style="margin-top: 20px">
# <h1> Question  #1):</h1>
# 
# <b>Use the function "train_test_split" to split up the data set such that 40% of the data samples will be utilized for testing, set the parameter "random_state" equal to zero. The output of the function should be the following:  "x_train_1" , "x_test_1", "y_train_1" and  "y_test_1".</b>
# </div>

# In[51]:


# Write your code below and press Shift+Enter to execute 
x_train_1, x_test_1, y_train_1, y_test_1 = train_test_split(x_data, y_data, test_size=0.40, random_state=0)


print("number of test samples :", x_test_1.shape[0])
print("number of training samples:",x_train_1.shape[0])


# Double-click <b>here</b> for the solution.
# 
# <!-- The answer is below:
# 
# x_train1, x_test1, y_train1, y_test1 = train_test_split(x_data, y_data, test_size=0.4, random_state=0) 
# print("number of test samples :", x_test1.shape[0])
# print("number of training samples:",x_train1.shape[0])
# 
# -->

# Let's import <b>LinearRegression</b> from the module <b>linear_model</b>.

# In[13]:


from sklearn.linear_model import LinearRegression


#  We create a Linear Regression object:

# In[14]:


lre=LinearRegression()


# we fit the model using the feature horsepower 

# In[66]:


lre.fit(x_train[['horsepower']], y_train)


# Let's Calculate the R^2 on the test data:

# In[67]:


lre.score(x_test[['horsepower']], y_test)


# we can see the R^2 is much smaller using the test data.

# In[68]:


lre.score(x_train[['horsepower']], y_train)


# <div class="alert alert-danger alertdanger" style="margin-top: 20px">
# <h1> Question  #2): </h1>
# <b> 
# Find the R^2  on the test data using 90% of the data for training data
# </b>
# </div>

# In[81]:


# Write your code below and press Shift+Enter to execute 
# Write your code below and press Shift+Enter to execute 
x_train1, x_test1, y_train1, y_test1 = train_test_split(x_data, y_data, test_size=0.10, random_state=0)
lre.fit(x_train1[['horsepower']],y_train1)
lre.score(x_test1[['horsepower']],y_test1), lre.score(x_train1[['horsepower']], y_train1)


# Double-click <b>here</b> for the solution.
# 
# <!-- The answer is below:
# 
# x_train1, x_test1, y_train1, y_test1 = train_test_split(x_data, y_data, test_size=0.1, random_state=0)
# lre.fit(x_train1[['horsepower']],y_train1)
# lre.score(x_test1[['horsepower']],y_test1)
# 
# -->

#  Sometimes you do not have sufficient testing data; as a result, you may want to perform Cross-validation. Let's  go over several methods that you can use for  Cross-validation. 

# <h2>Cross-validation Score</h2>

# Lets import <b>model_selection</b> from the module <b>cross_val_score</b>.

# In[23]:


from sklearn.model_selection import cross_val_score


# We input the object, the feature in this case ' horsepower', the target data (y_data). The parameter 'cv'  determines the number of folds; in this case 4. 

# In[82]:


Rcross = cross_val_score(lre, x_data[['horsepower']], y_data, cv=4)


# The default scoring is R^2; each element in the array has the average  R^2 value in the fold:

# In[25]:


Rcross


#  We can calculate the average and standard deviation of our estimate:

# In[26]:


print("The mean of the folds are", Rcross.mean(), "and the standard deviation is" , Rcross.std())


# We can use negative squared error as a score by setting the parameter  'scoring' metric to 'neg_mean_squared_error'. 

# In[27]:


-1 * cross_val_score(lre,x_data[['horsepower']], y_data,cv=4,scoring='neg_mean_squared_error')


# <div class="alert alert-danger alertdanger" style="margin-top: 20px">
# <h1> Question  #3): </h1>
# <b> 
# Calculate the average R^2 using two folds, find the average R^2 for the second fold utilizing the horsepower as a feature : 
# </b>
# </div>

# In[28]:


# Write your code below and press Shift+Enter to execute 
Rcross2 = cross_val_score(lre, x_data[['horsepower']], y_data, cv=2)
Rcross2[1]


# Double-click <b>here</b> for the solution.
# 
# <!-- The answer is below:
# 
# Rc=cross_val_score(lre,x_data[['horsepower']], y_data,cv=2)
# Rc[1]
# 
# -->

# You can also use the function 'cross_val_predict' to predict the output. The function splits up the data into the specified number of folds, using one fold to get a prediction while the rest of the folds are used as test data. First import the function:

# In[30]:


from sklearn.model_selection import cross_val_predict


# We input the object, the feature in this case <b>'horsepower'</b> , the target data <b>y_data</b>. The parameter 'cv' determines the number of folds; in this case 4. We can produce an output:

# In[31]:


yhat = cross_val_predict(lre,x_data[['horsepower']], y_data,cv=4)
yhat[0:5]


# <h1 id="ref2">Part 2: Overfitting, Underfitting and Model Selection</h1>
# 
# <p>It turns out that the test data sometimes referred to as the out of sample data is a much better measure of how well your model performs in the real world.  One reason for this is overfitting; let's go over some examples. It turns out these differences are more apparent in Multiple Linear Regression and Polynomial Regression so we will explore overfitting in that context.</p>

# Let's create Multiple linear regression objects and train the model using <b>'horsepower'</b>, <b>'curb-weight'</b>, <b>'engine-size'</b> and <b>'highway-mpg'</b> as features.

# In[83]:


lr = LinearRegression()
lr.fit(x_train[['horsepower', 'curb-weight', 'engine-size', 'highway-mpg']], y_train)


# Prediction using training data:

# In[84]:


yhat_train = lr.predict(x_train[['horsepower', 'curb-weight', 'engine-size', 'highway-mpg']])
yhat_train[0:5]


# Prediction using test data: 

# In[85]:


yhat_test = lr.predict(x_test[['horsepower', 'curb-weight', 'engine-size', 'highway-mpg']])
yhat_test[0:5]


# Let's perform some model evaluation using our training and testing data separately. First  we import the seaborn and matplotlibb library for plotting.

# In[86]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns


# Let's examine the distribution of the predicted values of the training data.

# In[87]:


Title = 'Distribution  Plot of  Predicted Value Using Training Data vs Training Data Distribution'
DistributionPlot(y_train, yhat_train, "Actual Values (Train)", "Predicted Values (Train)", Title)


# Figure 1: Plot of predicted values using the training data compared to the training data. 

# So far the model seems to be doing well in learning from the training dataset. But what happens when the model encounters new data from the testing dataset? When the model generates new values from the test data, we see the distribution of the predicted values is much different from the actual target values. 

# In[89]:


Title='Distribution  Plot of  Predicted Value Using Test Data vs Data Distribution of Test Data'
DistributionPlot(y_test,yhat_test,"Actual Values (Test)","Predicted Values (Test)",Title)


# Figur 2: Plot of predicted value using the test data compared to the test data. 

# <p>Comparing Figure 1 and Figure 2; it is evident the distribution of the test data in Figure 1 is much better at fitting the data. This difference in Figure 2 is apparent where the ranges are from 5000 to 15 000. This is where the distribution shape is exceptionally different. Let's see if polynomial regression also exhibits a drop in the prediction accuracy when analysing the test dataset.</p>

# In[90]:


from sklearn.preprocessing import PolynomialFeatures


# <h4>Overfitting</h4>
# <p>Overfitting occurs when the model fits the noise, not the underlying process. Therefore when testing your model using the test-set, your model does not perform as well as it is modelling noise, not the underlying process that generated the relationship. Let's create a degree 5 polynomial model.</p>

# Let's use 55 percent of the data for testing and the rest for training:

# In[92]:


x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.45, random_state=0)


# We will perform a degree 5 polynomial transformation on the feature <b>'horse power'</b>. 

# In[93]:


pr = PolynomialFeatures(degree=5)
x_train_pr = pr.fit_transform(x_train[['horsepower']])
x_test_pr = pr.fit_transform(x_test[['horsepower']])
pr


# Now let's create a linear regression model "poly" and train it.

# In[94]:


poly = LinearRegression()
poly.fit(x_train_pr, y_train)


# We can see the output of our model using the method  "predict." then assign the values to "yhat".

# In[95]:


yhat = poly.predict(x_test_pr)
yhat[0:5]


# Let's take the first five predicted values and compare it to the actual targets. 

# In[96]:


print("Predicted values:", yhat[0:4])
print("True values:", y_test[0:4].values)


# We will use the function "PollyPlot" that we defined at the beginning of the lab to display the training data, testing data, and the predicted function.

# In[97]:


PollyPlot(x_train[['horsepower']], x_test[['horsepower']], y_train, y_test, poly,pr)


# Figur 4 A polynomial regression model, red dots represent training data, green dots represent test data, and the blue line represents the model prediction. 

# We see that the estimated function appears to track the data but around 200 horsepower, the function begins to diverge from the data points. 

#  R^2 of the training data:

# In[98]:


poly.score(x_train_pr, y_train)


#  R^2 of the test data:

# In[99]:


poly.score(x_test_pr, y_test)


# We see the R^2 for the training data is 0.5567 while the R^2 on the test data was -29.87.  The lower the R^2, the worse the model, a Negative R^2 is a sign of overfitting.

# Let's see how the R^2 changes on the test data for different order polynomials and plot the results:

# In[100]:


Rsqu_test = []

order = [1, 2, 3, 4]
for n in order:
    pr = PolynomialFeatures(degree=n)
    
    x_train_pr = pr.fit_transform(x_train[['horsepower']])
    
    x_test_pr = pr.fit_transform(x_test[['horsepower']])    
    
    lr.fit(x_train_pr, y_train)
    
    Rsqu_test.append(lr.score(x_test_pr, y_test))

plt.plot(order, Rsqu_test)
plt.xlabel('order')
plt.ylabel('R^2')
plt.title('R^2 Using Test Data')
plt.text(3, 0.75, 'Maximum R^2 ')    


# We see the R^2 gradually increases until an order three polynomial is used. Then the  R^2 dramatically decreases at four.

# The following function will be used in the next section; please run the cell.

# In[102]:


def f(order, test_data):
    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=test_data, random_state=0)
    pr = PolynomialFeatures(degree=order)
    x_train_pr = pr.fit_transform(x_train[['horsepower']])
    x_test_pr = pr.fit_transform(x_test[['horsepower']])
    poly = LinearRegression()
    poly.fit(x_train_pr,y_train)
    PollyPlot(x_train[['horsepower']], x_test[['horsepower']], y_train,y_test, poly, pr)


# The following interface allows you to experiment with different polynomial orders and different amounts of data. 

# In[117]:


#interact(f, order=(4, 6, 1), test_data=(0.05, 0.95, 0.05))
pr1 = PolynomialFeatures(degree=2)
x_train_pr1 = pr1.fit_transform(x_train[['horsepower', 'curb-weight', 'engine-size', 'highway-mpg']])
x_test_pr1 = pr1.fit_transform(x_test[['horsepower', 'curb-weight', 'engine-size', 'highway-mpg']])
x_train_pr1.shape,  x_test_pr1.shape 
poly1 = LinearRegression()
poly1.fit(x_train_pr1,y_train)
yhat_test1=poly1.predict(x_test_pr1)
Title='Distribution  Plot of  Predicted Value Using Test Data vs Data Distribution of Test Data'
DistributionPlot(y_test, yhat_test1, "Actual Values (Test)", "Predicted Values (Test)", Title)


# <div class="alert alert-danger alertdanger" style="margin-top: 20px">
# <h1> Question  #4a):</h1>
# 
# <b>We can perform polynomial transformations with more than one feature. Create a "PolynomialFeatures" object "pr1" of degree two?</b>
# </div>

# Double-click <b>here</b> for the solution.
# 
# <!-- The answer is below:
# 
# pr1=PolynomialFeatures(degree=2)
# 
# -->

# <div class="alert alert-danger alertdanger" style="margin-top: 20px">
# <h1> Question  #4b): </h1>
# 
# <b> 
#  Transform the training and testing samples for the features 'horsepower', 'curb-weight', 'engine-size' and 'highway-mpg'. Hint: use the method "fit_transform" 
# ?</b>
# </div>

# Double-click <b>here</b> for the solution.
# 
# <!-- The answer is below:
# 
# x_train_pr1=pr.fit_transform(x_train[['horsepower', 'curb-weight', 'engine-size', 'highway-mpg']])
# 
# x_test_pr1=pr.fit_transform(x_test[['horsepower', 'curb-weight', 'engine-size', 'highway-mpg']])
# 
# -->

# <!-- The answer is below:
# 
# x_train_pr1=pr.fit_transform(x_train[['horsepower', 'curb-weight', 'engine-size', 'highway-mpg']])
# x_test_pr1=pr.fit_transform(x_test[['horsepower', 'curb-weight', 'engine-size', 'highway-mpg']])
# 
# -->

# <div class="alert alert-danger alertdanger" style="margin-top: 20px">
# <h1> Question  #4c): </h1>
# <b> 
# How many dimensions does the new feature have? Hint: use the attribute "shape"
# </b>
# </div>

# Double-click <b>here</b> for the solution.
# 
# <!-- The answer is below:
# 
# There are now 15 features: x_train_pr1.shape 
# 
# -->

# <div class="alert alert-danger alertdanger" style="margin-top: 20px">
# <h1> Question  #4d): </h1>
# 
# <b> 
# Create a linear regression model "poly1" and train the object using the method "fit" using the polynomial features?</b>
# </div>

# Double-click <b>here</b> for the solution.
# 
# <!-- The answer is below:
# 
# poly1=linear_model.LinearRegression().fit(x_train_pr1,y_train)
# 
# -->

#  <div class="alert alert-danger alertdanger" style="margin-top: 20px">
# <h1> Question  #4e): </h1>
# <b>Use the method  "predict" to predict an output on the polynomial features, then use the function "DistributionPlot"  to display the distribution of the predicted output vs the test data?</b>
# </div>

# Double-click <b>here</b> for the solution.
# 
# <!-- The answer is below:
# 
# yhat_test1=poly1.predict(x_test_pr1)
# Title='Distribution  Plot of  Predicted Value Using Test Data vs Data Distribution of Test Data'
# DistributionPlot(y_test, yhat_test1, "Actual Values (Test)", "Predicted Values (Test)", Title)
# 
# -->

# <div class="alert alert-danger alertdanger" style="margin-top: 20px">
# <h1> Question  #4f): </h1>
# 
# <b>Use the distribution plot to determine the two regions were the predicted prices are less accurate than the actual prices.</b>
# </div>

# Double-click <b>here</b> for the solution.
# 
# <!-- The answer is below:
# 
# The predicted value is lower than actual value for cars where the price  $ 10,000 range, conversely the predicted price is larger than the price cost in the $30, 000 to $40,000 range. As such the model is not as accurate in these ranges .
#     
# -->
# 
# <img src = "https://ibm.box.com/shared/static/c35ipv9zeanu7ynsnppb8gjo2re5ugeg.png" width = 700, align = "center">
# 

# <h2 id="ref3">Part 3: Ridge regression</h2> 

#  In this section, we will review Ridge Regression we will see how the parameter Alfa changes the model. Just a note here our test data will be used as validation data.

#  Let's perform a degree two polynomial transformation on our data. 

# In[130]:


pr=PolynomialFeatures(degree=2)
x_train_pr=pr.fit_transform(x_train[['horsepower', 'curb-weight', 'engine-size', 'highway-mpg','normalized-losses','symboling']])
x_test_pr=pr.fit_transform(x_test[['horsepower', 'curb-weight', 'engine-size', 'highway-mpg','normalized-losses','symboling']])


#  Let's import  <b>Ridge</b>  from the module <b>linear models</b>.

# In[120]:


from sklearn.linear_model import Ridge


# Let's create a Ridge regression object, setting the regularization parameter to 0.1 

# In[121]:


RigeModel=Ridge(alpha=0.1)


# Like regular regression, you can fit the model using the method <b>fit</b>.

# In[123]:


RigeModel.fit(x_train_pr, y_train)


#  Similarly, you can obtain a prediction: 

# In[125]:


yhat = RigeModel.predict(x_test_pr)


# Let's compare the first five predicted samples to our test set 

# In[126]:


print('predicted:', yhat[0:4])
print('test set :', y_test[0:4].values)


# We select the value of Alfa that minimizes the test error, for example, we can use a for loop. 

# In[127]:


Rsqu_test = []
Rsqu_train = []
dummy1 = []
ALFA = 10 * np.array(range(0,1000))
for alfa in ALFA:
    RigeModel = Ridge(alpha=alfa) 
    RigeModel.fit(x_train_pr, y_train)
    Rsqu_test.append(RigeModel.score(x_test_pr, y_test))
    Rsqu_train.append(RigeModel.score(x_train_pr, y_train))


# We can plot out the value of R^2 for different Alphas 

# In[128]:


width = 12
height = 10
plt.figure(figsize=(width, height))

plt.plot(ALFA,Rsqu_test, label='validation data  ')
plt.plot(ALFA,Rsqu_train, 'r', label='training Data ')
plt.xlabel('alpha')
plt.ylabel('R^2')
plt.legend()


# Figure 6:The blue line represents the R^2 of the test data, and the red line represents the R^2 of the training data. The x-axis represents the different values of Alfa 

# The red line in figure 6 represents the  R^2 of the test data, as Alpha increases the R^2 decreases; therefore as Alfa increases the model performs worse on the test data.  The blue line represents the R^2 on the validation data, as the value for Alfa increases the R^2 decreases.   

# <div class="alert alert-danger alertdanger" style="margin-top: 20px">
# <h1> Question  #5): </h1>
# 
# Perform Ridge regression and calculate the R^2 using the polynomial features, use the training data to train the model and test data to test the model. The parameter alpha should be set to  10.
# </div>

# In[133]:


# Write your code below and press Shift+Enter to execute 
RigeModel1=Ridge(alpha=10)
RigeModel1.fit(x_train_pr, y_train)
#yhat = RigeModel1.predict(x_test_pr)
#print('predicted:', yhat[0:4])
#print('test set :', y_test[0:4].values)
RigeModel1.score(x_test_pr, y_test)


# Double-click <b>here</b> for the solution.
# 
# <!-- The answer is below:
# 
# RigeModel = Ridge(alpha=0) 
# RigeModel.fit(x_train_pr, y_train)
# RigeModel.score(x_test_pr, y_test)
# 
# -->

# <h2 id="ref4">Part 4: Grid Search</h2>

# The term Alfa is a hyperparameter, sklearn has the class  <b>GridSearchCV</b> to make the process of finding the best hyperparameter simpler.

# Let's import <b>GridSearchCV</b> from  the module <b>model_selection</b>.

# In[135]:


from sklearn.model_selection import GridSearchCV


# We create a dictionary of parameter values:

# In[136]:


parameters1= [{'alpha': [0.001,0.1,1, 10, 100, 1000, 10000, 100000, 100000]}]
parameters1


# Create a ridge regions object:

# In[137]:


RR=Ridge()
RR


# Create a ridge grid search object 

# In[140]:


Grid1 = GridSearchCV(RR, parameters1,cv=4)


# Fit the model 

# In[141]:


Grid1.fit(x_data[['horsepower', 'curb-weight', 'engine-size', 'highway-mpg']], y_data)


# The object finds the best parameter values on the validation data. We can obtain the estimator with the best parameters and assign it to the variable BestRR as follows:

# In[142]:


BestRR=Grid1.best_estimator_
BestRR


#  We now test our model on the test data 

# In[143]:


BestRR.score(x_test[['horsepower', 'curb-weight', 'engine-size', 'highway-mpg']], y_test)


# <div class="alert alert-danger alertdanger" style="margin-top: 20px">
# <h1> Question  #6): </h1>
# Perform a grid search for the alpha parameter and the normalization parameter, then find the best values of the parameters
# </div>

# In[150]:


# Write your code below and press Shift+Enter to execute 
parameters2= [{'alpha': [0.001,0.1,1, 10, 100, 1000, 10000, 100000, 100000],'normalize': [True,False]}]
Grid2 = GridSearchCV(RR, parameters2,cv=4)
Grid2.fit(x_data[['horsepower', 'curb-weight', 'engine-size', 'highway-mpg']], y_data)
BestRR2=Grid2.best_estimator_
BestRR2,BestRR2.score(x_test[['horsepower', 'curb-weight', 'engine-size', 'highway-mpg']], y_test)


# Double-click <b>here</b> for the solution.
# 
# <!-- The answer is below:
# 
# parameters2= [{'alpha': [0.001,0.1,1, 10, 100, 1000,10000,100000,100000],'normalize':[True,False]} ]
# Grid2 = GridSearchCV(Ridge(), parameters2,cv=4)
# Grid2.fit(x_data[['horsepower', 'curb-weight', 'engine-size', 'highway-mpg']],y_data)
# Grid2.best_estimator_
# 
# -->

# <h1>Thank you for completing this notebook!</h1>

# <div class="alert alert-block alert-info" style="margin-top: 20px">
# <h2>Get IBM Watson Studio free of charge!</h2>
#     <p><a href="http://cocl.us/NotebooksPython101bottom"><img src="https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DA0101EN/Images/BottomAd.png" width="750" align="center"></a></p>
# </div>

# <h3>About the Authors:</h3>
# 
# This notebook was written by <a href="https://www.linkedin.com/in/mahdi-noorian-58219234/" target="_blank">Mahdi Noorian PhD</a>, <a href="https://www.linkedin.com/in/joseph-s-50398b136/" target="_blank">Joseph Santarcangelo</a>, Bahare Talayian, Eric Xiao, Steven Dong, Parizad, Hima Vsudevan and <a href="https://www.linkedin.com/in/fiorellawever/" target="_blank">Fiorella Wenver</a>.
# 
# <p><a href="https://www.linkedin.com/in/joseph-s-50398b136/" target="_blank">Joseph Santarcangelo</a> is a Data Scientist at IBM, and holds a PhD in Electrical Engineering. His research focused on using Machine Learning, Signal Processing, and Computer Vision to determine how videos impact human cognition. Joseph has been working for IBM since he completed his PhD.</p>

# <hr>
# <p>Copyright &copy; 2018 IBM Developer Skills Network. This notebook and its source code are released under the terms of the <a href="https://cognitiveclass.ai/mit-license/">MIT License</a>.</p>
