import re
import sys
import json
import pathlib
import argparse
from bs4 import BeautifulSoup


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfolder', type=str)
    parser.add_argument('globstr', type=str)
    parser.add_argument('outputfilename', type=str)
    args = parser.parse_args()

    data = extract_all_data(args.inputfolder, args.globstr)
    save_all_data(data, args.outputfilename)
    
    
def extract_all_data(inputfolder, globstr):
    htmls = {x.name: get_html(x) for x in pathlib.Path(inputfolder).glob(globstr)}
    data = {fn: extract_data(x) for fn, x in htmls.items()}
    return data


def save_all_data(obj, outputfilename):
    with open(outputfilename, 'w') as f:
        json.dump(obj, f, indent=4)
    

def get_html(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def extract_data(htmlcode: str) -> dict:
    soup = BeautifulSoup(htmlcode, features="lxml")
    body = soup.find('body')
    return dict(
        title = body.find(class_='title').text.strip(),
        timestamp = body.find(class_='heading').text.strip(),
        contents = body.find(class_='content').decode_contents().replace('<br/>', '\n'),
    )
        

if __name__ == '__main__':
    main()
