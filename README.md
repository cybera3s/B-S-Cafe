
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
<h1 align="center">Landing Page</h1>



<h1 align="center">Admin Panel Page</h1>









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
* ...



[comment]: <> (# Deployment)

[comment]: <> (<h3>)

[comment]: <> (    for visit deployed version go to this link)

[comment]: <> (    <a href="https://aivashop.pythonanywhere.com/en/">Aiva Shop</a>)

[comment]: <> (</h3>)


[comment]: <> (### Prerequisites)


[comment]: <> (* python &#40;Debian&#41;)
  
[comment]: <> (```sh)

[comment]: <> (sudo apt install python)

[comment]: <> (  ```)

[comment]: <> (for other platforms go to  [this link]&#40;https://www.python.org/downloads/&#41;)

[comment]: <> (### Installation)

[comment]: <> (Clone the repo)

[comment]: <> (   ```sh)

[comment]: <> (  git clone https://github.com/cybera3s/Ecommerce.git)

[comment]: <> (   ```)

[comment]: <> (change to root folder  )

[comment]: <> (    cd Ecommerce/)

[comment]: <> (create virtual environment )

[comment]: <> (    python -m virtualenv venv)

[comment]: <> (  activate venv)
  

[comment]: <> (    source venv/bin/activate)

[comment]: <> (install required packages)

[comment]: <> (    pip install -r requirements.txt)

[comment]: <> (change to Project folder  )

[comment]: <> (    cd ecommerce/)

[comment]: <> (extract static and media folder and remove archive file)

[comment]: <> (    tar -xf media-static.tar.xz && rm media-static.tar.xz)

[comment]: <> (create migrations)

[comment]: <> (    python manage.py makemigrations )


[comment]: <> (create database tables)

[comment]: <> (    python manage.py migrate)

[comment]: <> (create a super user)

[comment]: <> (    python manage.py createsuperuser)

[comment]: <> (load prepared data)

[comment]: <> (    python manage.py loaddata data.json)

[comment]: <> (compile translated messages)

[comment]: <> (    python manage.py compilemessages)

[comment]: <> (start Django development server)

[comment]: <> (    python manage.py runserver)

[comment]: <> (if everything goes well go to:  http://localhost:8000)
 


[comment]: <> (<!-- USAGE EXAMPLES -->)

[comment]: <> (## Usage)

[comment]: <> (if both development servers or up go to home page by)

[comment]: <> ( http://localhost:8000)

[comment]: <> (You can log in with the username and password you created for your superuser)

[comment]: <> (after log in you redirect to [students]&#40;http://localhost:8080/students&#41; table page you can add or delete any row of table)

[comment]: <> (Any other usage and information served API will find in http://127.0.0.1:8000/swagger/)

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
