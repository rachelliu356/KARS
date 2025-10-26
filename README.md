# KARS
Your own virtual speech coach.
Building off of Boson AI's Audio processing software, this program aids the deaf, hard of hearning, or anyone learning a new language in learning to speak by listening to users, giving speaking practice, and providing feedback on pronunciation in
a visual format. (maybe teach ipa?)

Installation Instructions:
- Python 3.8+
- Visual Studio Code
- Libraries/dependencies
	- streamlit
	- openai
	- os
	- base64
 
Create virtual environment:
Run the following code in order in the terminal of your code folder:
```
python -m venv my_env
./my_env/Scripts/activate
```

Run the following code in the terminal in the virtual environment to install the required libraries:
```  
pip install streamlit
pip install openai
pip install os
pip install base64
```

Run in terminal to activate the virtual environment:
```
./my_env/Scripts/activate
```

To run program, run in terminal:
```
streamlit run kars_v3.py
```
To stop running program, type CTRL+C in terminal.


      
