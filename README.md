# TVSphere

TVSphere is a Cross-Platform IP-TV app.


- [Installation / Build](#Installation--Build)

---


## Installation / Build

**Clone the Repository**
```commandline
git clone https://github.com/tibssy/TVSphere.git
cd TVSphere/
```

**Create and Activate a Virtual Environment**
```commandline
python3 -m venv venv
source venv/bin/activate
```

**Install Dependencies**
```commandline
pip install -r requirements.txt
```

**To build an APK using the fullscreen landscape template**
```commandline
flet build apk --template https://github.com/tibssy/TVSphere.git --template-ref flet-build-template-0.26-fullscreen-landscape
```

