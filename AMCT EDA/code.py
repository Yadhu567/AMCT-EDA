import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from scipy import stats

# Load dataset
data = pd.read_excel('data.xlsx')

# Displaying basic info about the dataset
data.info()

# Deleting the unnamed column
data = data.drop(columns=["Unnamed: 0"])

# Check for unique values in each column
for col in data.columns:
    print('-----------------------{}-----------------------'.format(col))
    print(data[col].unique())

# Descriptive statistics
data.describe()

# Data Cleaning
# Converting DOJ and DOL to datetime and calculating Tenure
data['DOJ'] = pd.to_datetime(data['DOJ'])
data['DOL'].replace(to_replace='present', value=pd.Timestamp.now(), inplace=True)
data['DOL'] = pd.to_datetime(data['DOL'])
data['Tenure'] = (data['DOL'] - data['DOJ']) / np.timedelta64(1, 'M')
data['Tenure'] = data['Tenure'].astype(int)

# Handling negative tenure values
# Creating Age column from DOB
data['DOB'] = pd.to_datetime(data['DOB'])
current_date = datetime.now()
data['Age'] = (current_date - data['DOB']).astype('<m8[Y]')

# Rows with Graduation Year as 0
data['GraduationYear'].replace(to_replace=0, value=2014, inplace=True)

# Replacing Specialization column values
Domains = {'computer engineering': 'CS', 'electronics and communication engineering': 'EE',
           'information technology': 'IT', 'computer science & engineering': 'CS', 
           'mechanical engineering': 'ME', 'electronics and electrical engineering': 'EE',
           'computer networking': 'CS', 'biomedical engineering': 'Other', 'electronics': 'EE',
           'computer science': 'CS'}
data['Specialization'].replace(Domains, inplace=True)

# Fuzzy matching for JobCity could be done with the fuzzywuzzy module
# Univariate Analysis
# Number of aspirants in each specialization
plt.figure(figsize=(14, 8))
sns.countplot(x='Specialization', data=data)
plt.title('Number of Aspirants in Each Specialization')
plt.show()

# Number of Males and Females
plt.figure(figsize=(14, 8))
sns.countplot(x='Gender', data=data)
plt.title('Number of Males and Females')
plt.show()

# Distribution of X, XII, and College percentages
plt.figure(figsize=(14, 8))
sns.histplot(data['10percentage'], kde=True, label='10th')
sns.histplot(data['12percentage'], kde=True, label='12th', color='orange')
sns.histplot(data['collegeGPA'], kde=True, label='College GPA', color='green')
plt.legend()
plt.title('Distribution of X, XII, and College Percentages')
plt.show()

# Bivariate Analysis
# Boxplot of Salary Vs Gender
plt.figure(figsize=(14, 8))
sns.boxplot(x='Gender', y='Salary', data=data)
plt.title('Boxplot of Salary vs Gender')
plt.show()

# Boxplot of Specialization Vs Salary
plt.figure(figsize=(14, 8))
sns.boxplot(x='Specialization', y='Salary', data=data)
plt.title('Boxplot of Specialization vs Salary')
plt.show()

# Testing Hypotheses
# CLAIM-1: Salary of fresh graduates in certain designations
claim_1_data = data[(data['Designation'].isin(["programmer analyst", "software engineer", 
                                               "hardware engineer", "associate engineer"])) & 
                    (data['Tenure']//12 == 0)]
plt.figure(figsize=(14, 8))
sns.barplot(x=claim_1_data['Designation'], y=claim_1_data['Salary']/100000, 
            hue=claim_1_data['Specialization'])
plt.title('Designation Vs Salary (In Lakhs)')
plt.show()

# CLAIM-2: Higher Education leads to better wages
data['Grad_level'] = ['UnderGrad' if x == 'B.Tech/B.E.' else 'PostGrad' for x in data['Degree']]
undergrad_sal = data.loc[data['Grad_level'] == 'UnderGrad', 'Salary']
postgrad_sal = data.loc[data['Grad_level'] == 'PostGrad', 'Salary']

t_statistic, p = stats.ttest_ind(undergrad_sal, postgrad_sal)
print("p-value:", p)
if p < 0.05:
    print("Reject the null hypothesis. There is a statistically significant difference in the average salary between undergraduates and postgraduates.")
else:
    print("Fail to reject the null hypothesis. There is no statistically significant difference.")
