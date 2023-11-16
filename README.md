## Test task

### Prerequisites 
- Python 3.8
### How to run:
Run next commands in project root
- python3 -m venv env
- . env/bin/activate (then (env) should appear on left part of terminal)
- pip install -r requirements.txt
- uvicorn main:app --reload --port 5050

Go to http://127.0.0.1:5050/docs#/default/get_github_info_get_github_links_post

Trigger that endpoint with all needed data and wait some time for code to execute.

example request:

    {
        "keywords": [
            "something",
            "&"
        ],
        "proxies": [
            "47.74.226.8:5001",
            "110.34.3.229:3128"
    
        ],
        "search_type": "Repositories"
    }

Example response :

    [
      {
        "url": "https://github.com/leitbogioro/Tools",
        "extra": {
          "language_stats": [
            {
              "Shell": "91.0%"
            },
            {
              "Batchfile": "8.4%"
            },
            {
              "HTML": "0.6%"
            }
          ],
          "author": "leitbogioro"
        }
      },
      {
        "url": "https://github.com/fangjian0423/springboot-analysis",
        "extra": {
          "language_stats": [
            {
              "Java": "100.0%"
            }
          ],
          "author": "fangjian0423"
        }
      },
      {
        "url": "https://github.com/sksalahuddin2828/C_Plus_Plus",
        "extra": {
          "language_stats": [
            {
              "C++": "100.0%"
            }
          ],
          "author": "sksalahuddin2828"
        }
      },
      {
        "url": "https://github.com/3c/share",
        "extra": {
          "language_stats": [],
          "author": "3c"
        }
      },
      {
        "url": "https://github.com/sksalahuddin2828/Java",
        "extra": {
          "language_stats": [
            {
              "Java": "100.0%"
            }
          ],
          "author": "sksalahuddin2828"
        }
      },
      {
        "url": "https://github.com/sksalahuddin2828/Pandas_Numpy_Matplotlib_Plotly",
        "extra": {
          "language_stats": [
            {
              "Python": "100.0%"
            }
          ],
          "author": "sksalahuddin2828"
        }
      },
      {
        "url": "https://github.com/sksalahuddin2828/JavaScript",
        "extra": {
          "language_stats": [
            {
              "JavaScript": "92.5%"
            },
            {
              "HTML": "7.0%"
            },
            {
              "CSS": "0.5%"
            }
          ],
          "author": "sksalahuddin2828"
        }
      },
      {
        "url": "https://github.com/sksalahuddin2828/C_Sharp",
        "extra": {
          "language_stats": [
            {
              "C#": "100.0%"
            }
          ],
          "author": "sksalahuddin2828"
        }
      },
      {
        "url": "https://github.com/sksalahuddin2828/Ruby_on_Rails",
        "extra": {
          "language_stats": [
            {
              "Ruby": "99.7%"
            },
            {
              "HTML": "0.3%"
            }
          ],
          "author": "sksalahuddin2828"
        }
      },
      {
        "url": "https://github.com/csstools/postcss-preset-env",
        "extra": {
          "language_stats": [
            {
              "CSS": "65.0%"
            },
            {
              "JavaScript": "35.0%"
            }
          ],
          "author": "csstools"
        }
      }
    ]

## TODO list
- add response models
- add unit tests