**Accounting Software for calculation of Closing Stock**

Frontend and backend info :

I have used Python Flask to create backend server, which serves the data from the db and json files stored in server directory.

for the frontend I have used Vue JS.

How to test:

Change current directory to repo that you cloned.

```
cd Accounting-Software-For-Closing-Stock
```

Now install node pakages using:

```
npm install
```

Before running vue app install flask server dependencies 

```
cd server
pip install -r Requirements.txt
python main.py
```

After starting flask server come back to the parent directory

```
cd ..
```

And start vue app:

```
npm run dev</code>
```


Key notes :

- There isn't any delete option to remove companies (will be added soon).
- Modify page dosen't follow application theme.
- Code migh be buggy so test it in development environment. 

