# Find a bar
## About the project
This is a training project (www.dvmn.org) that shows bars closest to provided location.
## Getting Started
### Prerequisites
* python3.6+
* API_KEY for HTTP Geokoder from https://developer.tech.yandex.ru/services/3/
### Installation
 Clone the repo
```sh
git clone git@github.com:vitaliy-baranov/dvmn_bars.git
cd dvmn_bars
```
Install and activate virtualenv
```sh
python3 -m venv .venv
source .venv/bin/activate
```
Install dependencies
```sh
python3 -m pip install -r requirements.txt
```
Get yandex api key from https://developer.tech.yandex.ru/services/ and store it into .env file
```
echo API_KEY=1234-345435-34534-34545 > .env
```
## Usage

```sh
python main.py
```
View the result on http://localhost:5000
## License

Distributed under the MIT License. 
