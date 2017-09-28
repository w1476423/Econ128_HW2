
# coding: utf-8

# In[2]:


import sqlite3
import pandas

sqlite_file = 'lahman2014.sqlite'
conn = sqlite3.connect(sqlite_file)  # connect to database and ingest the tables 

#getting familar with the data
query = "select * from Salaries WHERE teamID=='BAL' AND yearID = '1985' ;"

result = pandas.read_sql(query, conn)
result.head()


# In[3]:


createTable_query = "CREATE TABLE statsTbl AS SELECT Salaries.yearID, Teams.teamID, Teams.name, Salaries.salary, Teams.G, Teams.W, Teams.L FROM Salaries  JOIN Teams ON Salaries.yearID=Teams.yearID AND Salaries.teamID=Teams.teamID"

cursor = conn.cursor()
cursor.execute(createTable_query)
conn.commit()


# In[4]:


#new table 
query = "select * from statsTbl;"

result = pandas.read_sql(query, conn)
result.head()


# # Problem 1

# In[4]:


query = "SELECT teamID, yearID, SUM(salary) AS Total, CAST(W AS Float)/CAST(G AS Float)*100  AS WinningPercentage FROM statsTbl  GROUP BY teamID, yearID;"

result = pandas.read_sql(query, conn)
result.head()


# # Problem 2

# In[5]:


#Create a table based on the result from Problem 1
createTable_query2 = "CREATE TABLE WPOTS AS SELECT teamID, yearID, SUM(salary) AS Total, CAST(W AS Float)/CAST(G AS Float)*100  AS WinningPercentage FROM statsTbl  GROUP BY teamID, yearID;"

cursor = conn.cursor()
cursor.execute(createTable_query2)
conn.commit()


# In[6]:


# sample view of the table WPOTS
query = "SELECT * FROM WPOTS WHERE teamID='BAL';"

result = pandas.read_sql(query,conn)
result.head()


# In[8]:


#print out the max of WinningPercentage over Total Spending
query = "SELECT teamID, yearID, MAX(CAST(WinningPercentage/Total AS float)) AS wpots FROM WPOTS ORDER BY wpots DESC;"

result=pandas.read_sql(query,conn)
result.head()


# # Problem 3

# In[7]:


import matplotlib.pyplot as plt

query = "SELECT teamID, yearID, Total, WinningPercentage FROM WPOTS  WHERE teamID='OAK' AND yearID>=1990 AND yearID<=2014 GROUP BY teamID , yearID;"

result2 = pandas.read_sql(query, conn)
result2.head()
print result2
plt.plot(result2["yearID"],result2["Total"])
plt.title('Oakland Total Salary Spendings')
plt.ylabel('Total Spending ($), in 10^7')
plt.xlabel('Year')
plt.show()


# # Problem 4

# In[16]:


import matplotlib.pyplot as plt
import numpy as np

query = "SELECT teamID, yearID, Total, WinningPercentage FROM WPOTS  WHERE teamID='OAK' AND yearID>=1990 AND yearID<=2014 GROUP BY teamID , yearID;"

result2 = pandas.read_sql(query, conn)
#discretize year into five time periods
result2['yearCat'] = pandas.cut(result2["yearID"],5,labels=["p1","p2","p3","p4","p5"])
result2.head()

result=result2.groupby(['yearCat'])['Total'].mean() 
result3=result2.groupby(['yearCat'])['WinningPercentage'].mean()
print result
print result3

x = [1,2,3,4,5]
my_xticks = ["p1","p2","p3","p4","p5"]
plt.xticks(x, my_xticks)

plt.plot(result,result3,marker='o',  alpha=1, color='b')[0]
#plt.plot(x,result3)

plt.title('Oakland AvgSalary vs AvgWinningPercentage')
plt.ylabel('AvgWinningPercentage')
plt.xlabel('AvgSalary')
plt.show()


# In[19]:


query = "SELECT teamID, yearID, Total, WinningPercentage FROM WPOTS  WHERE teamID='OAK' AND yearID>=1990 AND yearID<=2014 GROUP BY teamID , yearID;"

result2 = pandas.read_sql(query, conn)
#discretize year into five time periods
result2['yearCat'] = pandas.cut(result2["yearID"],5,labels=["p1","p2","p3","p4","p5"])
result2.head()

result=result2.groupby(['yearCat'])['Total'].mean()
result3=result2.groupby(['yearCat'])['WinningPercentage'].mean()
x = [1,2,3,4,5]
my_xticks = ["p1","p2","p3","p4","p5"]
plt.xticks(x, my_xticks)

a=x,result3
b=x,result

plt.plot(b,a)
plt.title('OAK AvgWinningPercentage over AvgSalary')
plt.ylabel('AvgWinningPercentage')
plt.xlabel('AvgSalary')
plt.show()


# The team payroll increases pretty dramatically over the years, almost doubling from 1990 to 2014. Oakland's spending efficiency peaked in P3, but the efficiency has dropped after the peak. 
