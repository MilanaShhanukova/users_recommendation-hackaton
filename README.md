# users_recommendation-hackaton :computer:
This is a small project for a hackaton.

The main problem of this project was the absence of data, cause the company is only growing. Therefore I decided to create some logic in data. 
***all data is insignificant and shows only the logic. The more data we get, the better our algorithm works***

### logic of data 
1. User. 

:walking: For one user I recommend to save some info. My representation find in a [file](https://github.com/MilanaShhanukova/users_recommendation-hackaton/blob/main/users_info_prepare.py). 
 Each user has: 
* name 
* profession - how user identify themselves (developer, teacher or anyone) 
* spheres in which they are interested 
* interest - values how interested a person is in one sphere
* v - the rating of one person in a sphere
* projects which user creates 

2. Project 

:mortar_board: Each project has some important featurs. My representation of it find in a [file](https://github.com/MilanaShhanukova/users_recommendation-hackaton/blob/main/project_info.py)
* name 
* r - rank in other projects, how users like it 
* creators 
* label - idea or project, which is decided automatically in func "make idea project"
* main creator - who has created it 

All data is saved in Mongodb to make the process faster.  

### Recommendation 

In this project we use KNNearestNeighbors algorithm to recommend a user other creator in his/her team or project/idea to get. 

To recommend creators we use interests of other users and the experience/interest in it, therefore making teams balanced 
How it works like find in a [file](https://github.com/MilanaShhanukova/users_recommendation-hackaton/blob/main/predictions.py)

To recommend projects we use rating of this project and compare it with the rating of created project of one user. In the future I would like to make this system better and recommend projects regarding interest. 
How it works like find in a [file](https://github.com/MilanaShhanukova/users_recommendation-hackaton/blob/main/recommend_project.py)

### How it works 

You can see the logic of one user activity in [file](https://github.com/MilanaShhanukova/users_recommendation-hackaton/blob/main/interface.py)
For instance: 
here we check, what happens if one user like a project. 

Check what interest one user has:
*кулинария 0 

Here one user likes two projects in кулинария and программирование spheres

Check what interest one user has now 
*кулинария 0.02 
*программирование 0.02
