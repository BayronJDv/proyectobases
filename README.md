# proyectobases

## Autores 

Bayron Sebastian Jojoa Rosero_2242917

Alejandro Muñoz Guerrero_2242951

el siguiente proyecto fue consrtuido principalmente en python con el framework flask, se usa una base de datos postgres cuya configuracion
puede ser editada desde la carpeta config (verificar la ip,el nombre y contraseña de la base de datos )

## intrucciones Ejecucion

### Base de datos 

se corre el siguiente comando, la contraneña debe coincidir con el archivo en config en nuestro caso es pescado:

    docker run -e POSTGRES_PASSWORD=pescado -p 5432:5432 postgres

### Aplicacion web 

se hace el git clone a este repositorio, se inicia un entrono virtual, se activa el entrono  y se instalan los requerimientos
instrucciones para windows:

    git clone https://github.com/BayronJDv/proyectobases.git

    python -m venv venv 

    venv\Scripts\Activate.ps1

    pip install -r requirements.txt

Finalmente se puede iniciar la aplicacion ejecutando run.py 

    python run.py 

para visualizar la web revisar el puerto 5000, en el archivo run.py se crean automaticamente las tablas en la base de datos e inserta unos registros de prueba 
se puede probar las funcionalidades del cliente con el siguiente usuario

usuario de prueba : test-testing@test.com

contraseña : test**123
