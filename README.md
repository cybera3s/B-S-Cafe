
[![LinkedIn][linkedin-shield]][linkedin-url]



<div>
  <h1 align="center">Bitter & Sweet Cafe</h1>

  <p>
This is an example of an <b> Cafe </b> web application that offers online Cafe orders management.
It uses the Flask as Back-End server and also different Flask Extensions to improve and increase 
the speed and performance and Bootstrap for responsiveness and better display on different devices.

Challenges that I faced in this project:

- Component based development and architecture of placing files in order to reusability and increase speed
- Integrating <b> Celery </b> tasks to send email asynchronously in the background 
- Implementing Landing section of website as single-page-application (SPA)
- Integrating a self-customized admin panel to manage models

  
  </p>
</div>
<h1 align="center">Landing</h1>

![Landing_home](https://user-images.githubusercontent.com/74768669/182034911-e72b6cf7-1eb0-40d9-93a5-c109606e0909.png)
![Landing_menu](https://user-images.githubusercontent.com/74768669/182034938-65688959-d51c-41c5-be4d-0fcb443ac2b6.png)

<h1 align="center">Admin Panel</h1>

![admin_dashboard](https://user-images.githubusercontent.com/74768669/182035017-b5755ae5-d7e5-406e-a77d-6f220f98cb88.png)
![admin_menu](https://user-images.githubusercontent.com/74768669/182035298-947966d1-d530-42de-ba79-5af6e127d8f9.png)










### Built With
 * [Flask](https://flask.palletsprojects.com/en/2.1.x/)
 * [Bootstrap](https://getbootstrap.com)
 * [JQuery](https://jquery.com)
 
### Some of the Utilized Plugins in this project 
* [flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
* [flask-mail](https://flask-mail.readthedocs.io/en/latest/)
* [flask-migrate](https://flask-migrate.readthedocs.io/en/latest/)
* [flask-wtf](https://flask-wtf.readthedocs.io/en/1.0.x/)
* [Celery](https://docs.celeryq.dev/en/stable/index.html)
* [pytest](https://docs.pytest.org/en/7.1.x/)
* ...



[comment]: <> (# Deployment)

[comment]: <> (<h3>)

[comment]: <> (    for visit deployed version go to this link)

[comment]: <> (    <a href="https://aivashop.pythonanywhere.com/en/">Aiva Shop</a>)

[comment]: <> (</h3>)


### Prerequisites


* [Python](https://www.python.org/) +3.10
* [Redis](https://redis.io/)
* PIP
* virtualenv 
  ```sh
  pip install virtualenv
   ```
  


### Usage

Clone the repo

   ```sh

  git clone https://github.com/cybera3s/B-S-Cafe

   ```

change to root folder  

    cd B-S-Cafe

create virtual environment 

    python -m virtualenv venv

  activate venv
  
    source venv/bin/activate

install required packages

    pip install -r requirements.txt

change to Project folder  

    cd Cafe_project/


add and Open .env file to add Required Configurations:
```sh
nano .env
   ```
Add threse required Configurations to .env file:
```sh
MAIL_USERNAME=<your username>
MAIL_PASSWORD=<your email host password>
# redis://<username:<password>>@<host>:<port>
CELERY_BROKER_URL=<your Celery Broker Url>
CELERY_RESULT_BACKEND=<your celery reult backend url>
   ```
Save Your changes with CTRL+X then in the level of manage.py:

Run Celery Server: 
```sh
celery -A celery_runner.celery worker --loglevel=info
   ```

Start development Server

    python run.py 

if everything goes well visit site at: http://127.0.0.1:5000/

###CLI Management

You can access and manage project through command line:

set manage.py as flask application environment:

    export FLASK_APP=manage.py 
run flask shell:

    flask shell
in flask shell you have access to db, and all registered models in database

###Create New Cashier To Access Admin Panel:
run below command:

    flask create_new_cashier
Enter your personal information then you can visit [Login Page](http://127.0.0.1:5000/admin/login)
loggin with your newly created Email Address and Password

### Run Unit Tests
    flask tests


<!-- LICENSE -->

## License

Distributed under the GPL License




<!-- CONTACT -->

## Contact

Sajad Safa - cybera.3s@gmail.com

Project Link: [https://github.com/cybera3s/B-S-Cafe](https://github.com/cybera3s/B-S-Cafe)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/cybera3s/B-S-Cafe.svg?style=for-the-badge
[contributors-url]: https://github.com/cybera3s/B-S-Cafe/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/cybera3s/B-S-Cafe.svg?style=for-the-badge
[forks-url]: https://github.com/cybera3s/B-S-Cafe/network/members
[stars-shield]: https://img.shields.io/github/stars/cybera3s/B-S-Cafe.svg?style=for-the-badge
[stars-url]: https://github.com/cybera3s/B-S-Cafe/stargazers
[issues-shield]: https://img.shields.io/github/issues/cybera3s/B-S-Cafe.svg?style=for-the-badge
[issues-url]: https://github.com/cybera3s/B-S-Cafe/issues
[license-shield]: https://img.shields.io/github/license/cybera3s/Ecommerce.svg?style=for-the-badge
[license-url]: https://github.com/cybera3s/B-S-Cafe/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/cybera3s
