**Accounting Software for calculating Closing Stock**

Frontend and backend info :

I have used Python Flask to create a backend server, which serves the data from the db and json files stored in server directory.

for the frontend I have used Vue JS.

How to test:

Change current directory to repo that you cloned.

<code>cd Accounting-Software-For-Closing-Stock</code>

Now install node pakages using:

<code>npm install</code>

Before running vue app install flask server dependencies 

<code>cd server</code>
pip install -r Requirements.txt
python main.py</code>

After starting flask server come back to the parent directory

<code>cd ..</code>

And start vue app:

<code>npm run dev</code>


Key notes :

- There isn't any delete option to remove companies (will be added soon).
- Modify page dosen't follow application theme.
- Code migh be buggy so test it in development environment. 

