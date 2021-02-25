# MAYA-UM Timetable Scrapper

This is a mini side project to tinker around with Django and Selenium by web scraping FSKTM course timetable from MAYA as part of my self-learning prior to FYP.

## Getting Started with Django

### 1. Set up your Django project

If you are **cloning this repo**, run the following command preferably inside your virtual environment to install all dependencies:

- Using **venv**:
    ```Shell
    $ pip install -r requirements.txt # (Python 2)
    $ pip3 install -r requirements.txt # (Python 3)
    ``` 

Else, to **create your Django project** from scratch (make sure to have Django installed):

```Shell
$ django-admin startproject project_name
``` 

And then create a virtual environment (highly recommended):
- To **create** virtual environment:
    ```Shell
    $ python3 -m venv env_name # using Python's venv
    # or
    $ virtualenv env_name # using virtualenv
    ``` 
- To **activate** virtual environment (Linux/Mac OS):
    ```Shell
    $ source env_name/bin/activate
    ``` 

- Install all dependencies:
    ```Shell
    $ pip install -r requirements.txt # (Python 2)
    $ pip3 install -r requirements.txt # (Python 3)
    ``` 

Next, **navigate** into the newly created project folder. Then, **start a new Django app**. We will also **run migrations** and **start up the server**:

```Shell
$ cd project_name
$ python manage.py startapp app_name
$ python manage.py migrate
$ python manage.py runserver
``` 

If everything works well, we should see an instance of a Django application running on this address — http://localhost:8000

![alt text](https://scotch-res.cloudinary.com/image/upload/v1542486456/ia8jlkozut4uxwatnqwp.png)

### 2. Configure project settings

1. Add app inside INSTALLED_APPS (`settings.py`)

    Once you’ve created the app, you need to install it in your project. In `project_name/settings.py`, add the following line of code under `INSTALLED_APPS`:

    ```python
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'app_name',
    ]
    ```

    That line of code means that your project now knows that the app you just created exists.

2. Add templates folder directory in TEMPLATES  (`project_name/settings.py`)

    ```python
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': ['templates/'], # HERE
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]
    ```

2. Add static and media folder directory in STATIC_ROOT  (`project_name/settings.py`)

    ```python
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    ```

3. Add desired URL for the app (`project_name/urls.py`)

    ```python
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('(INSERT_URL)', include('APP_NAME.urls')),
    ]
    ```

4. Create new `urls.py` for the app (`app_name/urls.py`)

### 3. Configure app settings

1. **Create new template (**`app_name/templates/`**)**
    - You need to create the HTML template to display to the user after creating a view function.
    - Create a directory named **templates a**nd subsequently a file named `app_name.html` inside it:

        ```python
        # Create directory (if haven't)
        mkdir app_name/templates/

        # Create HTML template
        touch app_name/templates/app_name.html
        ```

2. **Create view function (FBV/CBV) in app's `views.py`**
    - Views in Django are a **collection of functions or classes** inside the `views.py` file in your app directory.
    - Each function or class handles the logic that gets processed each time a different URL is visited.

        ```python
        from django.shortcuts import render

        def view_name(request):
            return render(request, 'template_name.html', {})
        ```

    - The function defined is called a **view function**. When this function is called, it will render an HTML file called `app_name.html`.

3. **Add URL to app's `urls.py`**
    - The final step is to hook up your URLs so that you can visit the page you’ve just created.
    - Your project has a module called `urls.py` in which you need to include a URL configuration for the app. Inside `app_name/urls.py`, add the following:

        ```python
        from django.contrib import admin
        from django.urls import path, include

        urlpatterns = [
            path('', views.view_name, name="view_name"),
        ]
        ```

        - This looks for a module called `urls.py` inside the application and registers any URLs defined there.
        - Whenever you visit the root path of your URL (localhost:8000), the application’s URLs will be registered.

## Using Selenium in Django

### What is Web Scraping?

Web scraping is a technique for extracting information from the internet automatically using a software that simulates human web surfing.

### What is Selenium?

Selenium is a **free (open-source) automated testing framework** used to validate web applications across different browsers and platforms. It can be used for **automating web browsers to do a number of tasks** such as web-scraping.

### Installing Selenium

To install Selenium:
```Shell
    $ pip install selenium # (Python 2)
    $ pip3 install selenium # (Python 3)
``` 

### Installing Webdrivers

Selenium requires a **driver** to interface with the chosen browser. Firefox, for example, requires geckodriver, which needs to be installed before the below examples can be run. Note that the webdriver must be located in your `PATH`, e. g., place it in `/usr/bin` or `/usr/local/bin`.

Other supported browsers will have their own drivers available. Links to some of the more popular browser drivers are as follows:

- **Chrome**:	https://sites.google.com/a/chromium.org/chromedriver/downloads
- **Edge**:	    https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
- **Firefox**:	https://github.com/mozilla/geckodriver/releases
- **Safari**:	https://webkit.org/blog/6900/webdriver-support-in-safari-10/

For this project, I am using Chrome's webdriver called **Chromedriver**. There are multiple ways to install Chromedriver:
1. Using [**webdriver-manager**](https://pypi.org/project/webdriver-manager/) (recommended)
    
    - Install package:
        ```Shell
        $ pip install webdriver-manager # (Python 2)
        $ pip3 install webdriver-manager # (Python 3)
        ```     
    - Load package:
        ```python
        from selenium import webdriver
        from webdriver_manager.chrome import ChromeDriverManager

        driver = webdriver.Chrome(ChromeDriverManager().install())
        ```

2. **Manual download** from [Chrome's website](https://sites.google.com/a/chromium.org/chromedriver/downloads)

    - Load package:
        ```python
        from selenium import webdriver

        driver = webdriver.Chrome(executable_path='/path/to/chromedriver)
        ```