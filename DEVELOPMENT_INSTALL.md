# Installing development releases of Yokkaichi from git
- Installing the development releases with pipx (from git)
```
git clone https://github.com/Oreeeee/yokkaichi
cd yokkaichi/
git checkout master # for semi-stable code
git checkout dev # for development code. Might not run at all!!!!
pipx install . --force --include-deps
yokkaichi -v
```
- Temporarily installing the development releases with pipx (from git)
```
git clone https://github.com/Oreeeee/yokkaichi
cd yokkaichi/
git checkout master # for semi-stable code
git checkout dev # for development code. Might not run at all!!!!
pipx run --spec ./ yokkaichi -v
```
- Installing the development releases in virtual environment (from git)
```
git clone https://github.com/Oreeeee/yokkaichi
cd yokkaichi/
git checkout master # for semi-stable code
git checkout dev # for development code. Might not run at all!!!!
virtualenv .venv
source .venv/bin/activate # for Linux
.venv\bin\activate.bat # for Windows
pip install -e .
yokkaichi -v
```
